#!/bin/bash

RUN_PORT=8000

uvicorn main:app --host '0.0.0.0' --port ${RUN_PORT} --reload