PYTHON_PATH=/home/user/VSU/2_sem/UTP/vsu_task_core/.venv/bin/python3
MANAGE_PY_PATH=/home/user/VSU/2_sem/UTP/vsu_task_back/webapp/manage.py
DJANGO_CMD=$(PYTHON_PATH) ${MANAGE_PY_PATH}
# ======== Django ========
run:
	$(DJANGO_CMD) runserver

# ======== OpenAPI / Schema ========
schema:
	$(DJANGO_CMD) spectacular --file schema.yaml

# ======== Clear cache / pyc files ========
clean:
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -delete
