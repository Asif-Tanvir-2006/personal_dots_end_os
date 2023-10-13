#!/bin/bash
if nc -zw1 google.com 443; then
  echo "󰤨 "
else
  echo "󰤭 "
fi

