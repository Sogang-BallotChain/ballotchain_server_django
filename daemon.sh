if [ -f program.pid ]; then
	sudo kill -9 `cat program.pid`
fi

nohup sudo python3 manage.py runserver 0.0.0.0:80 > nohup.out 2>&1 & echo $! > program.pid
