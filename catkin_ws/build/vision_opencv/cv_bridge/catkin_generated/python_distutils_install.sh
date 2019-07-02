#!/bin/sh

if [ -n "$DESTDIR" ] ; then
    case $DESTDIR in
        /*) # ok
            ;;
        *)
            /bin/echo "DESTDIR argument must be absolute... "
            /bin/echo "otherwise python's distutils will bork things."
            exit 1
    esac
    DESTDIR_ARG="--root=$DESTDIR"
fi

echo_and_run() { echo "+ $@" ; "$@" ; }

echo_and_run cd "/home/sean_hastings/catkin_ws/src/vision_opencv/cv_bridge"

# ensure that Python install destination exists
echo_and_run mkdir -p "$DESTDIR/home/sean_hastings/catkin_ws/install/lib/python3/dist-packages"

# Note that PYTHONPATH is pulled from the environment to support installing
# into one location when some dependencies were installed in another
# location, #123.
echo_and_run /usr/bin/env \
    PYTHONPATH="/home/sean_hastings/catkin_ws/install/lib/python3/dist-packages:/home/sean_hastings/catkin_ws/build/lib/python3/dist-packages:$PYTHONPATH" \
    CATKIN_BINARY_DIR="/home/sean_hastings/catkin_ws/build" \
    "/home/sean_hastings/anaconda3/bin/python" \
    "/home/sean_hastings/catkin_ws/src/vision_opencv/cv_bridge/setup.py" \
    build --build-base "/home/sean_hastings/catkin_ws/build/vision_opencv/cv_bridge" \
    install \
    $DESTDIR_ARG \
    --install-layout=deb --prefix="/home/sean_hastings/catkin_ws/install" --install-scripts="/home/sean_hastings/catkin_ws/install/bin"
