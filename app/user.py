from fastapi import FastAPI, Depends, HTTPException, Query
from app.models import *
from app.schemas import *
from sqlalchemy import create_engine, func, and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, sessionmaker
from datetime import datetime

app = FastAPI()

engine = create_engine("mysql+pymysql://user:password@localhost/ptt_db")
SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 取得前50篇文章
@app.get("/api/posts", response_model=list[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # posts = db.query(PttPostsTable).all()
    posts = db.query(PttPostsTable).order_by(PttPostsTable.id.desc()).limit(50).all()
    if not posts:
        return []
    return posts


# 取得單一文章
@app.get("/api/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PttPostsTable).filter(PttPostsTable.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    print(post)
    return post

# 自定義過濾 發文時間 版面名稱 作者id 作者名字
@app.get("/api/statistics")
def get_statistics(
    post_date: str = Query(None, description="發文日期 (YYYY/MM/DD)"),
    board_name: str = Query(None, description="版面名稱"),
    author_ptt_id: str = Query(None, description="作者 PTT ID"),
    author_nickname: str = Query(None, description="作者 PTT 名字"),
    db: Session = Depends(get_db)
):
    query = db.query(func.count(PttPostsTable.id))

    filters = []

    if post_date:
        try:
            post_date = datetime.strptime(post_date, "%Y/%m/%d")
            filters.append(PttPostsTable.date >= post_date.strftime("%Y/%m/%d 00:00:00"))
        except ValueError:
            raise HTTPException(status_code=400, detail="錯誤格式 請使用YYYY/MM/DD.")

    if board_name:
        board = db.query(BoardTable).filter(BoardTable.board == board_name).first()
        if board:
            filters.append(PttPostsTable.board_id == board.id)
        else:
            return {"沒有這個版面椰"}

    if author_ptt_id:
        author = db.query(AuthorTable).filter(AuthorTable.author_ptt_id == author_ptt_id).first()
        if author:
            filters.append(PttPostsTable.author_id == author.id)
        else:
            return {"沒有這個作者"}

    if author_nickname:
        author = db.query(AuthorTable).filter(AuthorTable.author_nickname == author_nickname).first()
        if author:
            query = query.filter(PttPostsTable.author_id == author.id)
        else:
            return {"沒有這個作者"}

    if filters:
        query = query.filter(and_(*filters))

    total_posts = query.scalar()

    return {"文章總篇數": total_posts}

# 新增文章
@app.post("/api/posts", response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    board = db.query(BoardTable).filter(BoardTable.board == post.board_name).first()
    author = db.query(AuthorTable).filter(AuthorTable.author_ptt_id == post.author_ptt_id).first()

    if not author:
        db.add(AuthorTable(**{'author_nickname': post.author_nickname,
                              'author_ptt_id': post.author_ptt_id,}))
        db.commit()
    if not board:
        db.add(BoardTable(**{'board': post.board_name,
                             'url': f"https://www.ptt.cc/bbs/{post.board_name}/index.html"}))
        db.commit()


    db.refresh(board)
    db.refresh(author)

    db_post = PttPostsTable(
        title=post.title,
        link=post.link,
        date=post.date,
        content=post.content,
        board_id=board.id,
        author_id=author.id
    )

    db.add(db_post)
    try:
        db.commit()
        db.refresh(db_post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Post already exists")
    return db_post


# 刪除文章
@app.delete("/api/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(PttPostsTable).filter(PttPostsTable.id == id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return {"message": "Post deleted"}


# 修改文章
# todo : if author is exist/ not exist
@app.put("/api/posts/{id}", response_model=PostResponse)
def update_post(id: int, post_update: PostUpdate, db: Session = Depends(get_db)):
    db_post = db.query(PttPostsTable).filter(PttPostsTable.id == id).first()

    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")

    # 更新標題、連結、日期、內容
    db_post.title = post_update.title
    db_post.link = post_update.link
    db_post.date = post_update.date
    db_post.content = post_update.content

    # 更新 BoardTable（看是否需要變更版面）
    board = db.query(BoardTable).filter(BoardTable.board == post_update.board_name).first()
    if not board:
        board = BoardTable(board=post_update.board_name,
                           url=f"https://www.ptt.cc/bbs/{post_update.board_name}/index.html")
        db.add(board)
        db.commit()
        db.refresh(board)
    db_post.board_id = board.id

    # 更新 AuthorTable（看是否需要變更作者）
    author = db.query(AuthorTable).filter(AuthorTable.author_ptt_id == post_update.author_ptt_id).first()
    if not author:
        author = AuthorTable(author_ptt_id=post_update.author_ptt_id, author_nickname=post_update.author_nickname)
        db.add(author)
        db.commit()
        db.refresh(author)
    db_post.author_id = author.id

    try:
        db.commit()
        db.refresh(db_post)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Failed to update post due to integrity constraint")

    return db_post

