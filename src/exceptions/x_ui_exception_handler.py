from fastapi import HTTPException, status

class ThreeXUIExceptionHandler:
    validation_table: dict[str, dict] = {
        "record not found": {
            "detail": "Клиент не найден",
            "status_code": status.HTTP_404_NOT_FOUND
        },
        "at least one inbound is required": {
            "detail": "Необходимо указать хотя бы один inbound ID.",
            "status_code": status.HTTP_400_BAD_REQUEST
        },
        "client email is required": {
            "detail": "Поле Email является обязательным.",
            "status_code": status.HTTP_400_BAD_REQUEST
        }
    }

    @classmethod
    def handle_response(cls, response: dict):
        if not response or not isinstance(response, dict):
            return

        if response.get("success") is False:
            msg = response.get("msg", "").strip()

            if msg in cls.validation_table:
                error_info = cls.validation_table[msg]
                raise HTTPException(
                    status_code=error_info["status_code"],
                    detail=error_info["detail"]
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Ошибка: {msg}"
            )
