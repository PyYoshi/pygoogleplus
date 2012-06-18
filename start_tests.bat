chcp 932
nosetests --with-profile --profile-stats-file nose.prof tests.py
rem python -c "import hotshot.stats ; stats = hotshot.stats.load('nose.prof') ; stats.sort_stats('time', 'calls') ; stats.print_stats(20)"
hotshot2dot nose.prof| dot -Tpng -o profile.png

pause