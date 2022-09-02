#!/bin/sh

for i in $(seq 2 5)
do
	cp "title-1-active.xpm" "title-$i-active.xpm"
	sed -e "s/title_1/title_$i/g" -i "title-$i-active.xpm"
done

for f in *-active.xpm
do
	g="$(echo "$f" | sed -e 's/\(.*\)-active.xpm/\1-inactive.xpm/')"
	cp "$f" "$g"
	sed -e 's/active/inactive/g' -i "$g"
done
