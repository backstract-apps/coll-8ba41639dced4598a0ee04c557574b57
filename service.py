from sqlalchemy.orm import Session, aliased
from sqlalchemy import and_, or_
from typing import *
from fastapi import Request, UploadFile, HTTPException
import models, schemas
import boto3
import jwt
import datetime
import requests
from pathlib import Path


async def put_profile_id(
    db: Session,
    id: int,
    name: str,
    address: str,
    mobile: str,
    password: str,
    email: str,
):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.id == id))
    profile_edited_record = query.first()

    if profile_edited_record:
        for key, value in {
            "id": id,
            "name": name,
            "email": email,
            "mobile": mobile,
            "address": address,
            "password": password,
        }.items():
            setattr(profile_edited_record, key, value)

        db.commit()
        db.refresh(profile_edited_record)

        profile_edited_record = (
            profile_edited_record.to_dict()
            if hasattr(profile_edited_record, "to_dict")
            else vars(profile_edited_record)
        )
    res = {
        "profile_edited_record": profile_edited_record,
    }
    return res


async def delete_profile_id(db: Session, id: int):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        profile_deleted = record_to_delete.to_dict()
    else:
        profile_deleted = record_to_delete
    res = {
        "profile_deleted": profile_deleted,
    }
    return res


async def get_users(db: Session):

    query = db.query(models.Users)

    users_all = query.all()
    users_all = (
        [new_data.to_dict() for new_data in users_all] if users_all else users_all
    )
    res = {
        "users_all": users_all,
    }
    return res


async def get_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    users_one = query.first()

    users_one = (
        (users_one.to_dict() if hasattr(users_one, "to_dict") else vars(users_one))
        if users_one
        else users_one
    )

    res = {
        "users_one": users_one,
    }
    return res


async def put_users_id(db: Session, id: int, username: str, password: str, test: str):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))
    users_edited_record = query.first()

    if users_edited_record:
        for key, value in {
            "id": id,
            "test": test,
            "password": password,
            "username": username,
        }.items():
            setattr(users_edited_record, key, value)

        db.commit()
        db.refresh(users_edited_record)

        users_edited_record = (
            users_edited_record.to_dict()
            if hasattr(users_edited_record, "to_dict")
            else vars(users_edited_record)
        )
    res = {
        "users_edited_record": users_edited_record,
    }
    return res


async def delete_users_id(db: Session, id: int):

    query = db.query(models.Users)
    query = query.filter(and_(models.Users.id == id))

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        users_deleted = record_to_delete.to_dict()
    else:
        users_deleted = record_to_delete
    res = {
        "users_deleted": users_deleted,
    }
    return res


async def get_profile(db: Session):

    query = db.query(models.Profile)

    profile_all = query.all()
    profile_all = (
        [new_data.to_dict() for new_data in profile_all] if profile_all else profile_all
    )
    res = {
        "profile_all": profile_all,
    }
    return res


async def get_profile_id(db: Session, id: int):

    query = db.query(models.Profile)
    query = query.filter(and_(models.Profile.id == id))

    profile_one = query.first()

    profile_one = (
        (
            profile_one.to_dict()
            if hasattr(profile_one, "to_dict")
            else vars(profile_one)
        )
        if profile_one
        else profile_one
    )

    res = {
        "profile_one": profile_one,
    }
    return res


async def post_users(db: Session, username: str, password: str, test: str):

    import uuid

    try:
        id: str = str(uuid.uuid4())
        print(f"id: {id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    record_to_be_added = {"test": test, "password": password, "username": username}
    new_users = models.Users(**record_to_be_added)
    db.add(new_users)
    db.commit()
    db.refresh(new_users)
    user_details = new_users.to_dict()

    res = {
        "users_inserted_record": user_details,
        "uuid": id,
    }
    return res


async def post_user_records(db: Session, username: str, address: str, request: Request):
    header_authorization: str = request.headers.get("header-authorization")

    import uuid

    try:
        id: str = str(uuid.uuid4())
        print(f"id: {id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    record_to_be_added = {"address": address, "username": username}
    new_records = models.Records(**record_to_be_added)
    db.add(new_records)
    db.commit()
    db.refresh(new_records)
    users_records = new_records.to_dict()

    headers = {"authorization": header_authorization}
    auth = ("", "")
    payload = {"workspace_id": username, "collection_name": address}
    apiResponse = requests.get(
        "https://api.beemerbenzbentley.site/sigma/api/v1/collections/list/work_c71320e882214aebb9fe1c3952888e08",
        headers=headers,
        json=payload if "params" == "raw" else None,
    )
    test = apiResponse.json() if "dict" in ["dict", "list"] else apiResponse.text
    res = {
        "user_records": users_records,
        "uuid": id,
        "test": test,
    }
    return res


async def post_login(db: Session, email: str, password: str):

    query = db.query(models.Profile)
    query = query.filter(
        and_(models.Profile.email == email, models.Profile.password == password)
    )

    login = query.first()

    login = (
        (login.to_dict() if hasattr(login, "to_dict") else vars(login))
        if login
        else login
    )

    try:
        is_user_exist = None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    bs_jwt_payload = {
        "exp": int(
            (
                datetime.datetime.utcnow() + datetime.timedelta(seconds=100000)
            ).timestamp()
        ),
        "data": login,
    }

    jwt_1 = jwt.encode(
        bs_jwt_payload,
        "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI6MTUxNjIzOTAyMn0.KMUFsIDTnFmyG3nMiGM6H9FNFUROf3wh7SmqJp-QV30",
        algorithm="HS256",
    )

    if login == is_user_exist:

        raise HTTPException(status_code=404, detail="user not found")
    res = {
        "login": login,
        "jwt": jwt_1,
    }
    return res


async def delete_user_delete(db: Session, username: str, address: str):

    query = db.query(models.Records)
    query = query.filter(
        and_(models.Records.username == username, models.Records.address == address)
    )

    record_to_delete = query.first()
    if record_to_delete:
        db.delete(record_to_delete)
        db.commit()
        delete_records = record_to_delete.to_dict()
    else:
        delete_records = record_to_delete
    res = {
        "test": delete_records,
    }
    return res


async def post_profile(
    db: Session, name: str, address: str, mobile: str, password: str, email: str
):

    import uuid

    try:
        id: str = str(uuid.uuid4())
        print(f"id: {id}")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, str(e))

    record_to_be_added = {
        "name": name,
        "email": email,
        "mobile": mobile,
        "address": address,
        "password": password,
    }
    new_profile = models.Profile(**record_to_be_added)
    db.add(new_profile)
    db.commit()
    db.refresh(new_profile)
    add_a_record = new_profile.to_dict()

    res = {
        "profile_inserted_record": add_a_record,
    }
    return res
