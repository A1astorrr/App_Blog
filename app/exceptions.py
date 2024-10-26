from fastapi import HTTPException, status

PostNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Запись не найдена",
    )