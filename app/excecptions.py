from fastapi import HTTPException, status

PageNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Запись не найдена",
    )

ErrorAdding = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Ошибка при добавлении записи",
    )