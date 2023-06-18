#!/bin/sh

set -e

# Will fail; missing password and email
http POST localhost:8000/user/ username="Wendy"
# Will fail; missing email
http POST localhost:8000/user/ username="Wendy" password="123"

http POST localhost:8000/user/ username="Wendy" password="123" email="wendy@neverland.io"
http POST localhost:8000/user/ username="Peter Pen" password="pass123" email="peter@neverland.io"
http POST localhost:8000/user/ username="Captain Hook" password="crocodile123" email="hook@neverland.io"

http POST localhost:8000/hardware/ kind=1 owner_id=1
http POST localhost:8000/hardware/ kind=1 owner_id=1 comment="some comment"

http POST localhost:8000/hardware/ kind=1 owner_id=2
http POST localhost:8000/hardware/ kind=1 owner_id=2 comment="some comment"

http POST localhost:8000/hardware/ kind=1 owner_id=3
http POST localhost:8000/hardware/ kind=1 owner_id=3 comment="some comment"
