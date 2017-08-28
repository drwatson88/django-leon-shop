#!/bin/bash

# Переменная root-директории проекта
cd ../../../
PATH_ROOT=$(pwd);
echo $PATH_ROOT

# Разворачиваем тестовые данные
cd $PATH_ROOT
. ./venv3/bin/activate
cd ./apps/catalog/demo/
python ./create_objects.py $PATH_ROOT


