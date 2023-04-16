os: mac
and app.bundle: com.flyingmeat.Acorn7
-
new (from | with) clipboard: key(cmd-alt-n)

export: key(cmd-alt-s)

copy merged: key(ctrl-cmd-c)

# https://flyingmeat.com/acorn/docs-7.0/keyboard_shortcuts.html
move: key(v)
zoom: key(z)
crop: key(c)
pan: key(h)
select: key(m)
magic wand: key(w)
brush: key(b)
pencil: key(n)
fill: key(k)
erase: key(e)
gradient: key(g)
text: key(t)
circle text: key(t:2)
path text: key(t:3)
pen: key(p)
anchor: key(a)
reset control points: key(C)
line: key(;)
rectangle: key(r)
oval: key(o)
color | eyedropper: key(ctrl-c)

trim to edges: key(cmd-ctrl-t)

toggle fill: key(F)
toggle stroke: key(B)

toggle guides: key(cmd-alt-;)
new guide: user.menu_select("View|Guides and Grids|New Guide…")

toggle palettes: key(tab)

snap to guides: user.menu_select("View|Guides and Grids|Snap To Guides")
snap to selection: user.menu_select("View|Guides and Grids|Snap To Selection")
snap to grid: user.menu_select("View|Guides and Grids|Snap To Grid")
snap to shapes: user.menu_select("View|Guides and Grids|Snap To Shapes")
snap to layers: user.menu_select("View|Guides and Grids|Snap To Layers")
snap to canvas: user.menu_select("View|Guides and Grids|Snap To Canvas")

one hundred percent: edit.zoom_reset()
two hundred percent: key(cmd-2)
four hundred percent: key(cmd-3)
eight hundred percent: key(cmd-4)
fifty percent: key(cmd-5)
