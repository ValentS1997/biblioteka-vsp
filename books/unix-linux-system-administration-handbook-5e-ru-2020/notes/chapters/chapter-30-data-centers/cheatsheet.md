# Шпаргалка: Data centers

## 1. Reliability starts below the OS

~~~text
service
→ compute/network/storage
→ racks/cabling
→ power
→ cooling
→ physical site
→ people/process
~~~

Cloud resources still depend on physical infrastructure.

## 2. Rack discipline

Prefer:
- standard racks;
- traceable cable paths;
- accessible overhead network cabling;
- predictable rack orientation.

Avoid:
- hidden cable maze;
- untraceable underfloor network cabling;
- ad-hoc floor/table placement.

## 3. Power chain

~~~text
utility power
→ UPS
→ generator / alternate source
→ rack distribution
→ equipment
~~~

UPS bridges short outages.
Generator supports longer outages while fuel remains.

## 4. Test backup power

Chapter recommends:
- backup-power testing every 6 months;
- maintenance at least annually.

These are chapter-era recommendations.
Current site/vendor requirements:
[Needs confirmation].

## 5. Plan power per rack

Do not size only from floor area.

~~~text
equipment inventory
→ measured/estimated watts
→ rack power class
→ power zone
→ matching cooling
~~~

Chapter examples span 6–40 kW/rack.

## 6. Measure actual power

Prefer actual consumption over nameplate maximum.

Measure where feasible:
- facility;
- row;
- rack;
- device.

## 7. kVA / kW

Chapter approximation:

~~~text
kVA ≈ kW / 0.85
~~~

Real power factor is site/device specific.

## 8. PUE

~~~text
PUE =
total facility power
/
IT equipment power
~~~

Lower means less non-IT overhead.

PUE does not directly measure server efficiency.

## 9. Remote power control

Useful for remote recovery, but high risk.

Before action:
- verify device;
- verify outlet;
- verify maintenance window;
- verify impact.

Exact API/CLI:
[Needs confirmation].

## 10. Cooling load

Components:
- roof/walls/windows;
- electronics;
- lighting;
- people.

Electronics:
~~~text
watts × 3.412 = BTUH
~~~

Cooling:
~~~text
BTUH / 12000 = tons
~~~

Chapter worked example uses additional 50% allowance.
Do not treat as universal engineering rule.

## 11. Temperature

Chapter cites ASHRAE 2012:

~~~text
18–27 °C
~~~

measured at server air intakes.

Current guidance:
[Needs confirmation].

## 12. Hot / cold aisles

~~~text
cold aisle
→ server intake
→ server
→ hot exhaust
→ hot aisle
→ heat removal
~~~

Prevent hot exhaust recirculation into intake.

## 13. Humidity

Chapter cites:

~~~text
8–60%
~~~

Too dry:
- static electricity.

Too humid:
- condensation;
- corrosion;
- short-circuit risk.

Current hardware/facility requirements:
[Needs confirmation].

## 14. Environmental monitoring

Monitor unattended facility conditions:
- temperature;
- power;
- noise.

Alerts should reach responders remotely.

## 15. Reliability vocabulary

~~~text
N    = required capacity
N+1  = one spare unit
2N   = full duplicate capacity
~~~

Tier/redundancy labels help compare designs.

Redundancy alone does not guarantee availability.

## 16. Failure-domain separation

Higher-redundancy design should avoid one power/cooling fault disabling both primary and redundant paths.

~~~text
redundancy
+ physical separation
+ operations discipline
~~~

## 17. Physical threat model

Natural:
- fire;
- flood;
- earthquake;
- severe weather.

Human / industrial:
- crime;
- sabotage;
- nearby hazardous facilities.

## 18. Physical defense in depth

~~~text
site selection
→ perimeter
→ facility entrance
→ cage/rack
→ surveillance
~~~

One failed control should not expose everything.

## 19. Visitor access

Verify:
- identity;
- authorization;
- purpose.

Unverified technician/vendor:
~~~text
no authorization
→ no access
~~~

## 20. Rack access

Colocation/shared environment:
- separate rack/cage control;
- MFA access;
- rack-level surveillance.

Least physical privilege applies.

## 21. Toolkit

Useful chapter categories:
- hand tools;
- DMM;
- infrared thermometer;
- RJ-45 tools;
- spare cables/connectors;
- ESD wrist strap;
- network analyzer/laptop;
- emergency contacts.

## 22. Acceptance checklist

Before calling facility ready:
- racks/cables serviceable;
- power modeled per rack;
- actual load measurable;
- UPS coverage present;
- long-outage strategy defined;
- backup power tested;
- cooling load checked;
- hot/cold airflow verified;
- temperature/humidity monitored;
- environmental alerts tested safely;
- access boundaries documented;
- emergency contacts/tools available.

Exact electrical/code/fire/HVAC compliance:
[Needs confirmation].
