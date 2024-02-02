from fastapi import HTTPException


EmailAlreadyTaken = HTTPException(
    status_code=400, detail="User with this email already exists."
)

UserNotFound = HTTPException(
    status_code=404, detail="User with passed parameters not found."
)

PublicatonNotFound = HTTPException(
    status_code=404, detail="Publucation with passed id not found."
)


CredentialsException = HTTPException(
    status_code=401,
    detail="Could not validate credentials",
)
