from figstyle import *
H = 1000
fig, ax = canvas(H)
title(ax, "Receiver state machine")
OFF, HELD, TR = (230, 450), (760, 450), (1280, 450)
for (x, y), n, s in [(OFF, "OFF", "panel dark"), (HELD, "HELD", "sweeping, direction latched"), (TR, "TRAILING", "counting down 4 cycles")]:
    box(ax, x, y, 260, 104, n, s, head_size=17, sub_size=12)
# boot
arrow(ax, 70, 300, OFF[0] - 95, OFF[1] - 54)
label(ax, 70, 285, "reset / boot", size=12, color=GREY, ha="left")
# OFF -> HELD
arrow(ax, OFF[0] + 130, 450, HELD[0] - 130, 450)
label(ax, 495, 430, "press LEFT or RIGHT", size=13)
# HELD -> TRAILING
arrow(ax, HELD[0] + 130, 450, TR[0] - 130, 450)
label(ax, 1020, 430, "release", size=13)
# HELD self loop
arrow(ax, HELD[0] - 50, 398, HELD[0] + 50, 398, rad=-1.6)
label(ax, HELD[0], 262, "new or different press:\nrestart, direction = pressed", size=12.5, linespacing=1.3)
# TRAILING -> HELD
arrow(ax, TR[0], 398, HELD[0] + 90, 398, rad=0.45)
label(ax, 1040, 205, "any press: restart HELD\nin the new direction", size=12.5, linespacing=1.3)
# TRAILING -> OFF
arrow(ax, TR[0], 502, OFF[0] + 10, 502, rad=-0.18)
label(ax, 755, 640, "TRAILING_CYCLES elapse (4 × 1688 ms ≈ 6.75 s): dark", size=13)
# failsafe
arrow(ax, HELD[0] - 10, 502, OFF[0] - 20, 504, color=AMBER, dashed=True, rad=-0.35)
label(ax, 470, 728, "link quiet > 1000 ms (LINK_TIMEOUT): dark, failsafe", size=13, color=AMBER)
label(ax, 470, 754, "TRAILING drops to OFF the same way", size=12, color=GREY)
footer(fig, ax, 830, "the receiver's three-state activation logic. Any button press, from either state, cancels "
       "whatever is playing and starts a fresh hold; there is no toggle and no separate off command. The "
       "dashed amber path is the firmware failsafe: if the ESP-NOW link goes quiet for more than "
       "LINK_TIMEOUT, the panel forces itself dark rather than freezing lit.")
save(fig, "state_machine_diagram.png")
