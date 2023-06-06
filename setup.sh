#!/usr/bin/env bash


ARCH=$(uname -m)

install_geckodriver() {
  gecko_driver="misc/geckodriver-v0.33.0-linux64.tar.gz"
  if [[ ${ARCH} -eq "aarch64" ]]; then
    gecko_driver="misc/geckodriver-v0.33.0-linux-aarch64.tar.gz"
  fi

  tar -zxvf "${gecko_driver}" -C /usr/local/bin
}


collect_static() {
  if [[ ! -d "static" ]]; then
    mkdir static
  fi

  python manage.py collectstatic --noinput
}

cleanup() {
  rm -rfv misc/
}

install_geckodriver
collect_static


cleanup
