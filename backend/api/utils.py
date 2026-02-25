# ============================================================
# api/utils.py — Custom DRF Exception Handler
# ============================================================
# Ensures all errors return a consistent JSON format with
# a "detail" field — matching what the frontend expects.
# ============================================================

from rest_framework.views import exception_handler


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        # Flatten DRF's error format into a single "detail" string
        if isinstance(response.data, dict):
            # Already has "detail" key — leave it
            if "detail" not in response.data:
                # Merge all field errors into one readable string
                messages = []
                for field, errors in response.data.items():
                    if isinstance(errors, list):
                        messages.append(f"{field}: {', '.join(str(e) for e in errors)}")
                    else:
                        messages.append(f"{field}: {errors}")
                response.data = {"detail": "; ".join(messages)}
        elif isinstance(response.data, list):
            response.data = {"detail": "; ".join(str(e) for e in response.data)}

    return response
