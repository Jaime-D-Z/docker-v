import os
import sys

def _get_env_int(name, default):
	try:
		return int(os.getenv(name, default))
	except Exception:
		return int(default)

def try_import(name, install_hint):
	try:
		module = __import__(name)
		return module
	except ImportError:
		print(f"Missing dependency '{name}'. Install with: {install_hint}", file=sys.stderr)
		return None

def test_postgres():
	psycopg2 = try_import('psycopg2', 'pip install psycopg2-binary')
	if not psycopg2:
		return False

	host = os.getenv('DB_HOST', 'localhost')
	port = _get_env_int('DB_PORT', '5432')
	db = os.getenv('DB_NAME', 'main_db')
	user = os.getenv('DB_USER', 'devuser')
	password = os.getenv('DB_PASS', 'devpass')
	timeout = _get_env_int('POSTGRES_TIMEOUT', '5')

	try:
		conn = psycopg2.connect(host=host, port=port, dbname=db, user=user, password=password, connect_timeout=timeout)
		conn.close()
		print(f"Postgres ({host}:{port}/{db}) - TODO BIEN")
		return True
	except Exception as e:
		print(f"Postgres ({host}:{port}/{db}) - FALLO: {e}")
		return False

def test_redis():
	redis_mod = try_import('redis', 'pip install redis')
	if not redis_mod:
		return False

	host = os.getenv('REDIS_HOST', 'localhost')
	port = _get_env_int('REDIS_PORT', '6379')
	db = _get_env_int('REDIS_DB', '0')
	password = os.getenv('REDIS_PASSWORD', None) or None
	timeout = _get_env_int('REDIS_TIMEOUT', '5')

	try:
		client = redis_mod.Redis(host=host, port=port, db=db, password=password, socket_connect_timeout=timeout)
		client.ping()
		print(f"Redis ({host}:{port}/{db}) - TODO BIEN")
		return True
	except Exception as e:
		print(f"Redis ({host}:{port}/{db}) - FALLO: {e}")
		return False

def main():
	pg_ok = test_postgres()
	rd_ok = test_redis()

	if pg_ok and rd_ok:
		print("Todos los controles pasaron.")
		sys.exit(0)
	else:
		print("Una o más comprobaciones fallaron.")
		sys.exit(1)

if __name__ == '__main__':
	main()
