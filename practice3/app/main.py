from fastapi import FastAPI, Depends, HTTPException
from typing import List
from sqlmodel import select
from app.connection import init_db, get_session
from app.models import (
    Warrior, WarriorDefault, WarriorResponse,
    Skill, SkillCreate,
    Profession, ProfessionCreate
)

# from typing import List, TypedDict
# from sqlmodel import select
# from app.connection import init_db, get_session
# # from app.models import Warrior, WarriorDefault, WarriorResponse, Skill, Profession
# from app.models import Warrior, Skill, Profession, WarriorDefault, WarriorProfessions


app = FastAPI()


# создание таблиц прис старте, если их пока нет
@app.on_event("startup")
def on_startup():
    init_db()


# ============================================================================

# post запрос на создание warrior
@app.post("/warriors", response_model=WarriorResponse, summary="Создать нового воина")
def create_warrior(warrior: WarriorDefault, session=Depends(get_session)):
    db_warrior = Warrior(**warrior.dict())
    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return db_warrior

# get запрос на получение списка воинов
@app.get("/warriors", response_model=List[WarriorResponse], summary="Получить список всех воинов")
def list_warriors(session=Depends(get_session)):
    return session.exec(select(Warrior)).all()

# get запрос на получения воина по id
@app.get("/warriors/{warrior_id}", response_model=WarriorResponse, summary="Получить воина по ID (с вложенными навыками)")
def get_warrior(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    return warrior

# patch запрос для частичного обновления данных
@app.patch("/warriors/{warrior_id}", response_model=WarriorResponse, summary="Частично обновить воина")
def update_warrior(warrior_id: int, warrior: WarriorDefault, session=Depends(get_session)):
    db_warrior = session.get(Warrior, warrior_id)
    if not db_warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")

    # берём только те поля, что пришли (exclude_unset)
    update_data = warrior.dict(exclude_unset=True)
    for key, val in update_data.items():
        setattr(db_warrior, key, val)

    session.add(db_warrior)
    session.commit()
    session.refresh(db_warrior)
    return db_warrior

# запрос на удаление воина
@app.delete("/warriors/{warrior_id}", summary="Удалить воина")
def delete_warrior(warrior_id: int, session=Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    if not warrior:
        raise HTTPException(status_code=404, detail="Warrior not found")
    session.delete(warrior)
    session.commit()
    return {"ok": True}

# ============================================================================

@app.post("/skills", response_model=Skill, summary="Создать новый навык")
def create_skill(skill: SkillCreate, session=Depends(get_session)):
    db_skill = Skill(**skill.dict())
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill

@app.get("/skills", response_model=List[Skill], summary="Получить все навыки")
def list_skills(session=Depends(get_session)):
    return session.exec(select(Skill)).all()

@app.get("/skills/{skill_id}", response_model=Skill, summary="Получить навык по id")
def get_skill(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill

@app.patch("/skills/{skill_id}", response_model=Skill, summary="Обновить навык")
def update_skill( skill_id: int, skill: SkillCreate, session=Depends(get_session)):
    db_skill = session.get(Skill, skill_id)
    if not db_skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    skill_data = skill.dict(exclude_unset=True)
    for key, val in skill_data.items():
        setattr(db_skill, key, val)
    session.add(db_skill)
    session.commit()
    session.refresh(db_skill)
    return db_skill

@app.delete("/skills/{skill_id}", summary="Удалить навык")
def delete_skill(skill_id: int, session=Depends(get_session)):
    skill = session.get(Skill, skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    session.delete(skill)
    session.commit()
    return {"ok": True}

# ============================================================================

@app.post("/warriors/{warrior_id}/skills/{skill_id}", summary="Привязать навык воину")
def link_skill_to_warrior(warrior_id: int, skill_id:   int, session=    Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    skill   = session.get(Skill, skill_id)
    if not (warrior and skill):
        raise HTTPException(status_code=404, detail="Warrior or Skill not found")

    # orm сам создаст запись в skill_warrior_link
    warrior.skills.append(skill)
    session.add(warrior)
    session.commit()
    return {"ok": True}

@app.delete("/warriors/{warrior_id}/skills/{skill_id}", summary="Отвязать навык от воина")
def unlink_skill_from_warrior(warrior_id: int, skill_id:   int, session=    Depends(get_session)):
    warrior = session.get(Warrior, warrior_id)
    skill   = session.get(Skill, skill_id)
    if not (warrior and skill):
        raise HTTPException(status_code=404, detail="Warrior or Skill not found")

    warrior.skills.remove(skill)
    session.add(warrior)
    session.commit()
    return {"ok": True}

# ============================================================================

@app.post("/professions", response_model=Profession, summary="Создать профессию")
def create_profession(prof: ProfessionCreate, session=Depends(get_session)):
    db_prof = Profession(**prof.dict())
    session.add(db_prof)
    session.commit()
    session.refresh(db_prof)
    return db_prof

@app.get("/professions", response_model=List[Profession], summary="Список профессий")
def list_professions(session=Depends(get_session)):
    return session.exec(select(Profession)).all()

# ============================================================================



# post запрос на создание warrior
# @app.post("/warrior")
# def warriors_create(warrior: WarriorDefault, session=Depends(get_session)) -> TypeDict('Response', {"status": int, "data": Warrior}):
#     warrior = Warrior.model_validate(warrior)
#     session.add(warrior)
#     session.commit()
#     session.refresh(warrior)
#     return {"status": 200, "data": warrior}


# get запрос на получение списка воинов
# @app.get("/warriors_list")
# def warriors_list(session=Depends(get_session)) -> List[Warrior]:
#     return session.exec(select(Warrior)).all()


# get запрос на получения воина по id
# @app.get("/warrior/{warrior_id}", response_model=WarriorProfessions)
# def warriors_get(warrior_id: int, session=Depends(get_session)) -> Warrior:
#     warrior = session.get(Warrior, warrior_id)
#     return warrior


# patch запрос для частичного обновления данных
# @app.patch("/warrior{warrior_id}")
# def warrior_update(warrior_id: int, warrior: WarriorDefault, session=Depends(get_session)) -> WarriorDefault:
#     db_warrior = session.get(Warrior, warrior_id)
#     if not db_warrior:
#         raise HTTPException(status_code=404, detail="Warrior not found")
#     warrior_data = warrior.model_dump(exclude_unset=True)
#     for key, value in warrior_data.items():
#         setattr(db_warrior, key, value)
#     session.add(db_warrior)
#     session.commit()
#     session.refresh(db_warrior)
#     return db_warrior


# @app.delete("/warrior/delete{warrior_id}")
# def warrior_delete(warrior_id: int, session=Depends(get_session)):
#     warrior = session.get(Warrior, warrior_id)
#     if not warrior:
#         raise HTTPException(status_code=404, detail="Warrior not found")
#     session.delete(warrior)
#     session.commit()
#     return {"ok": True}


# @app.get("/professions_list")
# def professions_list(session=Depends(get_session)) -> List[Profession]:
#     return session.exec(select(Profession)).all()


# @app.get("/profession/{profession_id}")
# def profession_get(profession_id: int, session=Depends(get_session)) -> Profession:
#     return session.get(Profession, profession_id)


# @app.post("/profession")
# def profession_create(prof: ProfessionDefault, session=Depends(get_session)) -> TypedDict('Response', {"status": int, "data": Profession}):
#     prof = Profession.model_validate(prof)
#     session.add(prof)
#     session.commit()
#     session.refresh(prof)
#     return {"status": 200, "data": prof}



























# CRUD для воинов
# @app.post("/warriors", response_model=WarriorResponse)
# def create_warrior(
#     warrior: WarriorDefault, session=Depends(get_session)
# ):
#     db_warrior = Warrior(**warrior.model_dump())
#     session.add(db_warrior)
#     session.commit()
#     session.refresh(db_warrior)
#     return db_warrior

# @app.get("/warriors", response_model=List[WarriorResponse])
# def list_warriors(session=Depends(get_session)):
#     warriors = session.exec(select(Warrior)).all()
#     return warriors

# @app.get("/warriors/{warrior_id}", response_model=WarriorResponse)
# def get_warrior(warrior_id: int, session=Depends(get_session)):
#     warrior = session.get(Warrior, warrior_id)
#     if not warrior:
#         raise HTTPException(status_code=404, detail="Warrior not found")
#     return warrior

# @app.patch("/warriors/{warrior_id}", response_model=WarriorResponse)
# def update_warrior(
#     warrior_id: int,
#     warrior: WarriorDefault,
#     session=Depends(get_session)
# ):
#     db_warrior = session.get(Warrior, warrior_id)
#     if not db_warrior:
#         raise HTTPException(status_code=404, detail="Warrior not found")
#     update_data = warrior.model_dump(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(db_warrior, key, value)
#     session.add(db_warrior)
#     session.commit()
#     session.refresh(db_warrior)
#     return db_warrior

# @app.delete("/warriors/{warrior_id}")
# def delete_warrior(warrior_id: int, session=Depends(get_session)):
#     warrior = session.get(Warrior, warrior_id)
#     if not warrior:
#         raise HTTPException(status_code=404, detail="Warrior not found")
#     session.delete(warrior)
#     session.commit()
#     return {"ok": True}

# # также для Skill и Profession