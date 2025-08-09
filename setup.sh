#!/usr/bin/env bash



ARCH=$(uname -m)
GECKO_DRIVER_DOWNLOAD_URL_AARCH64="https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux-aarch64.tar.gz"
GECKO_DRIVER_DOWNLOAD_URL_X86_64="https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz"


# Get GECKO_DRIVER_DOWNLOAD_URL from environment variable, empty by default
GECKO_DRIVER_DOWNLOAD_URL="${GECKO_DRIVER_DOWNLOAD_URL:-}"

# If GECKO_DRIVER_DOWNLOAD_URL is empty, set based on ARCH
if [[ -z "${GECKO_DRIVER_DOWNLOAD_URL}" ]]; then
  if [[ ${ARCH} == "aarch64" ]]; then
    GECKO_DRIVER_DOWNLOAD_URL=${GECKO_DRIVER_DOWNLOAD_URL_AARCH64}
  else
    GECKO_DRIVER_DOWNLOAD_URL=${GECKO_DRIVER_DOWNLOAD_URL_X86_64}
  fi
fi

GECKO_DRIVER_INSTALL="misc/geckodriver.tar.gz"

install_geckodriver() {
  if [[ ! -f "${gecko_driver}" ]]; then
    wget "${GECKO_DRIVER_DOWNLOAD_URL}" -O "${GECKO_DRIVER_INSTALL}"
  fi

  tar -zxvf "${GECKO_DRIVER_INSTALL}" -C /usr/local/bin
}


collect_static() {
  if [[ ! -d "static" ]]; then
    mkdir static
  fi

  python manage.py collectstatic --noinput
}

generate_secret_key() {
  # Generate a 50-character Django secret key
  secret_key=$(python -c 'import secrets; import string; print("".join(secrets.choice(string.ascii_letters + string.digits + string.punctuation) for _ in range(50)))')
  # Replace SECRET_KEY_TO_REPLACE in settings_prod.py
  sed -i "" "s/SECRET_KEY_TO_REPLACE/${secret_key}/" chrono_manager/settings_prod.py
}

run_uwsgi() {
  uwsgi --ini uwsgi.ini
}

cleanup() {
  rm -rfv misc/
}



# Unified entrypoint
main() {
  if [[ "$1" == "run" ]]; then
    run_uwsgi
  else
    install_geckodriver
    collect_static
    generate_secret_key
    cleanup
  fi
}

main "$@"
