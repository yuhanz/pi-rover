goal:
dx = 0, u = 0

can be measured:
- theta'
- ax
- ay

ax = g * sin(theta) + u * cos(theta)
ay = g * cos(theta) + u * sin(theta)
theta" = (m*l**2) * u + g * sin(theta)

=>
u* ax = u* g * sin(theta) + u * u * cos(theta)
g* ay = g* g * cos(theta) + u * g * sin(theta)

=> g * ay - u * ax = (g * g - u * u)* cos(theta)
=> cos(theta) = (g*ay - u*ax) / (g**2 - u**2)

Then I got observation [cos(theta); sin(theta); theta']

Let x = [cos(theta); sin(theta); theta']
