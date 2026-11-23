import io, sys, re

def mount(name, dur):
    p = 'index.html'
    s = io.open(p, encoding='utf-8').read()
    if 'id="el-%s"' % name in s:
        print('already mounted:', name); return
    # compute cumulative start: sum of existing clip durations
    durs = [int(x) for x in re.findall(r'data-duration="(\d+)"', s)]
    # root duration is the first data-duration (135); clips follow
    root = durs[0]
    starts = [int(x) for x in re.findall(r'data-start="(\d+)"', s)]
    start = max([a + b for a, b in zip(starts, durs[1:])] + [0])
    mount = (
        '      <div\n'
        '        id="el-%s"\n'
        '        data-composition-id="%s"\n'
        '        data-composition-src="compositions/%s.html"\n'
        '        data-start="%d"\n'
        '        data-duration="%d"\n'
        '        data-track-index="0"\n'
        '      ></div>\n'
    ) % (name, name, name, start, dur)
    anchor = '      <div\n        id="el-simplex"'
    assert anchor in s
    s = s.replace(anchor, mount + anchor)
    re.sub(r'(id="root"\s*\n\s*data-composition-id="root"\s*\n\s*data-start="0"\s*\n\s*data-duration=")\d+(")',
               r'\g<1>%d\g<2>' % (start + dur), s, count=1)
    io.open(p, 'w', encoding='utf-8').write(s)
    print('mounted %s at %ds (root -> %ds)' % (name, start, start + dur))

if __name__ == '__main__':
    mount(sys.argv[1], int(sys.argv[2]))
