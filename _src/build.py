#!/usr/bin/env python3
"""Faithful Rides LLC — static site generator.

Edit content here, then run:  python3 _src/build.py
Every page is written as <slug>/index.html so the old site's URLs keep working.
Built by Truly Digital Solutions, LLC (TruTech) · Build TT-FR-2026-05
"""
import html, json, os, re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_ID = 'TT-FR-2026-05'
DOMAIN = 'https://www.faithfulridesllc.com'

B = {
    'name': 'Faithful Rides LLC',
    'phone': '(252) 503-2978', 'tel': '+12525032978',
    'fax': '1 (910) 333-0128',
    'email': 'contact@faithfulridesllc.com',
    'street': '625 College St.', 'city': 'Jacksonville, NC 28540',
    'map': 'https://maps.google.com/maps?q=625+College+St.%2C+Jacksonville%2C+NC+28540',
    'npi': '1760299101',
    'sister': 'https://www.rapturereadyhomecare.com',
}
HOURS = [('Monday – Saturday', '10:00 am – 5:00 pm'), ('Sunday', '2:00 pm – 6:00 pm')]

esc = html.escape


def icon(name, cls='ic'):
    p = {
        'phone': '<path d="M5 4h3.5l1.6 4.2-2.2 1.4a11 11 0 0 0 6.5 6.5l1.4-2.2L20 15.5V19a1.5 1.5 0 0 1-1.6 1.5A16.5 16.5 0 0 1 3.5 5.6 1.5 1.5 0 0 1 5 4Z"/>',
        'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
        'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
        'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        'shield': '<path d="M12 3 5 6v5.5c0 4.3 3 7.8 7 9.5 4-1.7 7-5.2 7-9.5V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
        'flag': '<path d="M5 21V4M5 4h11l-2 4 2 4H5"/>',
        'card': '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3 10h18M7 15h4"/>',
        'tag': '<path d="M3 12V4h8l10 10-8 8L3 12Z"/><circle cx="7.5" cy="8.5" r="1.5"/>',
        'smile': '<circle cx="12" cy="12" r="8.5"/><path d="M8.5 14a4.5 4.5 0 0 0 7 0M9 9.5h.01M15 9.5h.01"/>',
        'heart': '<path d="M12 20s-7.5-4.6-7.5-10.1A4.3 4.3 0 0 1 12 7.3a4.3 4.3 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20Z"/>',
        'timer': '<circle cx="12" cy="13" r="7.5"/><path d="M12 9v4l2.5 1.5M9.5 3h5"/>',
        'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'back': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
        'home': '<path d="M4 11 12 4l8 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
        'id': '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M5.8 16c.6-1.6 1.8-2.4 3.2-2.4s2.6.8 3.2 2.4M14.5 10h4M14.5 13.5h3"/>',
        'fax': '<path d="M7 9V4h10v5"/><rect x="3.5" y="9" width="17" height="8" rx="2"/><path d="M7 14h10v6H7z"/>',
        'star': '<path d="m12 3.8 2.5 5.1 5.6.8-4 4 .9 5.6L12 16.7l-5 2.6.9-5.6-4-4 5.6-.8L12 3.8Z"/>',
        'repeat': '<path d="M4 12a7 7 0 0 1 12-5l2 2M20 12a7 7 0 0 1-12 5l-2-2"/><path d="M18 4v5h-5M6 20v-5h5"/>',
        'wheel': '<circle cx="10" cy="15" r="5"/><path d="M10 4.5a1.5 1.5 0 1 0 0 .01M10 7v5h5l2 5h2"/>',
        'care': '<path d="M12 20s-7.5-4.6-7.5-10.1A4.3 4.3 0 0 1 12 7.3a4.3 4.3 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20Z"/><path d="M12 10v5M9.5 12.5h5"/>',
    }[name]
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'


# ---------------------------------------------------------------------------
# Content (all facts from the current site, brochure and ads)
# ---------------------------------------------------------------------------
WHY = [
    ('flag', 'Veteran owned and operated', 'A veteran-owned, family-oriented company that cares about the people and community we serve.'),
    ('timer', 'Prompt and reliable', 'We arrive on time and make sure you get home safely.'),
    ('smile', 'Friendly, professional drivers', 'Every driver is screened and held to our high standards of courtesy and care.'),
    ('card', 'Most insurances accepted', 'We accept most major insurances to keep your out-of-pocket costs down. Private pay is welcome too.'),
    ('tag', 'Fair, competitive rates', 'We keep our prices competitive so every ride is a good value.'),
    ('heart', '100% satisfaction guarantee', 'If you are ever unhappy with a ride, we will do everything we can to make it right.'),
]

SERVICES = [
    ('doctor', 'Doctor’s appointments', 'assets/img/doctor.webp', 'An older man being helped from a car into his wheelchair',
     'Your appointments matter. Don’t stress about getting there — with Faithful Rides, you or your loved one will arrive safely and on time, and get home again.'),
    ('therapy', 'Physical therapy', 'assets/img/therapy.webp', 'An older man smiling during aquatic physical therapy',
     'Trips to physical therapy made easy, safe and stress-free. Our drivers help door to door so you can focus on feeling better — one ride at a time.'),
    ('errands', 'Daily errands', 'assets/img/grocery.webp', 'A driver helping an older woman push her cart in a grocery store',
     'Safe rides to and from the everyday things — the grocery store, the pharmacy, the bank. Our drivers pay special attention to see that everyone arrives safely.'),
    ('veterans', 'Veteran transportation', 'assets/img/veteran.webp', 'A veteran being helped into a vehicle',
     'We honor your service with dependable rides to all your appointments, errands and daily needs — with the dignity and respect you deserve.'),
    ('partners', 'Healthcare partners', 'assets/img/partners.webp', 'A team of doctors and nurses',
     'Partner with us so your patients get to their appointments on time, every time. Professional, HIPAA-aware drivers and a smooth experience for your team and theirs.'),
]

TRIPS = ['Doctor visits and follow-ups', 'Dialysis', 'Physical therapy and rehabilitation', 'Chemotherapy or infusion', 'Lab work and routine tests',
         'Hospital discharge', 'Pharmacy pick-ups', 'Adult day and wellness programs', 'Groceries and errands']

STEPS = [
    ('Call or request a ride', f'Call {B["phone"]} or send a ride request online with your questions.'),
    ('Share the details', 'Tell us the appointment date, time and location, plus where to pick you up.'),
    ('We confirm your ride', 'We call to confirm and make sure everything is ready for your trip.'),
    ('We arrive and help', 'Your driver arrives on time and assists you throughout the journey — then home again.'),
]

REVIEWS = [
    ('After my surgery, I needed reliable transport to physical therapy. Faithful Rides never let me down. As a veteran, it means a lot to be treated with dignity and respect. They truly live up to their name.', 'James T.', 'U.S. Army veteran'),
    ('They transported me to multiple medical appointments, and every single ride was handled with the kind of professionalism you rarely see anymore. They arrived on time, every time. What stood out most was how seamlessly they worked with the medical staff, coordinating arrivals, drop-offs and assistance. Five stars without hesitation.', 'Matthew Feehan', ''),
    ('I live alone and don’t have family nearby, so getting to the grocery store or the pharmacy used to be stressful. With Faithful Rides, I can run errands and keep my independence — it’s a blessing I didn’t know I needed.', 'Linda R.', 'Age 72'),
]

ARTICLES = [
    ('newsroom', 'Medicare vs. Medicare Advantage: what you need to know', 'assets/img/medicare.webp',
     'How each option works, and how it can affect the transportation benefits available to you.'),
    ('nemt-101-everything-you-need-to-know-about-our-services', 'NEMT 101: everything you need to know about our services', 'assets/img/ramp.webp',
     'New to non-emergency medical transportation? What it is, who it’s for and how to book a ride.'),
    ('5-key-benefits-of-non-emergency-medical-transportation-for-senior-citizens', '5 key benefits of non-emergency medical transportation for seniors', 'assets/img/walker.webp',
     'Better access to care, fewer missed appointments and more independence — here’s why NEMT matters.'),
]

NAV = [('our-services', 'Services'), ('about-us', 'About'), ('community-on-the-move', 'Community on the Move'), ('contact-us', 'Contact')]


class Page:
    def __init__(self, slug):
        self.slug = slug
        self.depth = 0 if slug == '' else slug.count('/') + 1

    def u(self, path):
        pre = '../' * self.depth
        if path == '':
            return pre or './'
        if path.startswith(('http', 'mailto:', 'tel:', '#')):
            return path
        if '#' in path and not path.startswith('assets/'):
            p, h = path.split('#', 1)
            return (pre + p + '/' if p else (pre or './')) + '#' + h
        if path.startswith('assets/') or '.' in path.split('/')[-1]:
            return pre + path
        return pre + path + '/'


def hours_html(sep='<br>'):
    return sep.join(f'{d}: {h}' for d, h in HOURS)


def schema():
    data = {
        '@context': 'https://schema.org', '@type': 'LocalBusiness', 'additionalType': 'https://en.wikipedia.org/wiki/Non-emergency_medical_transportation',
        'name': B['name'], 'url': DOMAIN + '/', 'telephone': '+1-252-503-2978', 'faxNumber': '+1-910-333-0128', 'email': B['email'],
        'image': DOMAIN + '/assets/img/hero-lift.webp', 'logo': DOMAIN + '/assets/img/logo.png',
        'address': {'@type': 'PostalAddress', 'streetAddress': '625 College St.', 'addressLocality': 'Jacksonville',
                    'addressRegion': 'NC', 'postalCode': '28540', 'addressCountry': 'US'},
        'areaServed': 'Jacksonville, NC',
        'openingHoursSpecification': [
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'], 'opens': '10:00', 'closes': '17:00'},
            {'@type': 'OpeningHoursSpecification', 'dayOfWeek': 'Sunday', 'opens': '14:00', 'closes': '18:00'}],
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'NPI', 'value': B['npi']},
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def shell(pg, title, desc, body, active=None, og_img='assets/img/hero-lift.webp'):
    canonical = DOMAIN + '/' + (pg.slug + '/' if pg.slug else '')
    nav = ''.join(f'<li><a href="{pg.u(s)}"{" aria-current=page" if active == s else ""}>{t}</a></li>' for s, t in NAV)
    return f'''<!doctype html>
<!-- Built by Truly Digital Solutions, LLC (TruTech) · https://trutech.us · Build {BUILD_ID} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="Truly Digital Solutions, LLC (TruTech)">
<meta name="generator" content="TruTech · trutech.us">
<meta name="trutech-build" content="{BUILD_ID}">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/{og_img}">
<meta name="theme-color" content="#1b2a5e">
<link rel="icon" href="{pg.u('assets/img/favicon.png')}">
<link rel="apple-touch-icon" href="{pg.u('assets/img/apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,600;0,700;1,400&family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,600;12..96,700&display=swap">
<link rel="stylesheet" href="{pg.u('assets/site.css')}">
<script>try{{var s=localStorage.getItem('fr-size');if(s)document.documentElement.dataset.size=s}}catch(e){{}}</script>
<script src="{pg.u('assets/site.js')}" defer></script>
{schema() if pg.slug == '' else ''}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="util">
  <div class="wrap util__in">
    <p class="util__status" data-status><span class="dot" aria-hidden="true"></span><span data-status-text>Mon – Sat 10 am – 5 pm, Sun 2 – 6 pm</span></p>
    <div class="util__right">
      <div class="size" role="group" aria-label="Text size">
        <span class="size__label">Text size</span>
        <button type="button" data-size-btn="1" aria-pressed="true" aria-label="Normal text">A</button>
        <button type="button" data-size-btn="2" aria-pressed="false" aria-label="Larger text">A</button>
        <button type="button" data-size-btn="3" aria-pressed="false" aria-label="Largest text">A</button>
      </div>
      <a class="util__phone" href="tel:{B['tel']}">{icon('phone')}<span>{B['phone']}</span></a>
    </div>
  </div>
</div>
<header class="hdr" data-hdr>
  <div class="wrap hdr__in">
    <a class="brand" href="{pg.u('')}" aria-label="Faithful Rides, home">
      <img src="{pg.u('assets/img/logo.webp')}" alt="" width="408" height="166">
      <span class="brand__name">Faithful Rides<small>Non-emergency medical transportation</small></span>
    </a>
    <nav class="nav" aria-label="Main" data-nav>
      <ul>{nav}</ul>
      <a class="btn btn--primary nav__cta" href="{pg.u('schedule-a-ride')}">Schedule a ride</a>
      <a class="nav__phone" href="tel:{B['tel']}">{icon('phone')}{B['phone']}</a>
    </nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu" data-menu-btn><span class="menu-btn__bars" aria-hidden="true"></span><span data-menu-label>Menu</span></button>
  </div>
</header>
<main id="main">
{body}
</main>
{footer(pg)}
</body>
</html>
'''


def footer(pg):
    hrs = ''.join(f'<li>{icon("clock") if i == 0 else "<span class=ic></span>"}<span>{d}<br>{h}</span></li>' for i, (d, h) in enumerate(HOURS))
    return f'''<footer class="ftr">
  <div class="wrap ftr__grid">
    <div class="ftr__about">
      <a class="brand brand--ftr" href="{pg.u('')}"><img src="{pg.u('assets/img/logo.webp')}" alt="" width="408" height="166"><span class="brand__name">Faithful Rides<small>Driven by care, guided by faith</small></span></a>
      <p>Veteran-owned, family-oriented non-emergency medical transportation in Jacksonville, NC. On time, in comfort, with a steady hand at the door.</p>
    </div>
    <div>
      <h2 class="ftr__h">Visit or call</h2>
      <ul class="ftr__list">
        <li>{icon('pin')}<a href="{B['map']}" target="_blank" rel="noopener">{B['street']}<br>{B['city']}</a></li>
        <li>{icon('phone')}<a href="tel:{B['tel']}">{B['phone']}</a></li>
        <li>{icon('fax')}<span>Fax {B['fax']}</span></li>
        <li>{icon('mail')}<a href="mailto:{B['email']}">{B['email']}</a></li>
      </ul>
    </div>
    <div>
      <h2 class="ftr__h">Hours</h2>
      <ul class="ftr__list">{hrs}
        <li>{icon('id')}<span>NPI {B['npi']}<br><small>For insurance use</small></span></li>
      </ul>
    </div>
    <div>
      <h2 class="ftr__h">Explore</h2>
      <ul class="ftr__links">
        <li><a href="{pg.u('schedule-a-ride')}">Schedule a ride</a></li>
        <li><a href="{pg.u('our-services')}">Our services</a></li>
        <li><a href="{pg.u('about-us')}">About us</a></li>
        <li><a href="{pg.u('community-on-the-move')}">Community on the Move</a></li>
        <li><a href="{pg.u('resources')}">Rider resources</a></li>
        <li><a href="{pg.u('contact-us')}">Contact us</a></li>
        <li><a href="{B['sister']}" target="_blank" rel="noopener">Rapture Ready Home Care</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap ftr__legal">
    <p>© <span data-year>{date.today().year}</span> Faithful Rides LLC. All rights reserved.</p>
    <p><a href="{pg.u('privacy-policy')}">Privacy policy</a> <span aria-hidden="true">/</span> Site by <a href="https://trutech.us" target="_blank" rel="noopener">TruTech</a></p>
  </div>
</footer>'''


# ---------------------------------------------------------------------------
# Sections
# ---------------------------------------------------------------------------
def page_head(pg, title, lead, crumb=None, img=None):
    c = f'<p class="crumb"><a href="{pg.u(crumb[0])}">{icon("back")}{crumb[1]}</a></p>' if crumb else ''
    art = f'<div class="phead__img"><img src="{pg.u(img)}" alt="" width="1400" height="933"></div>' if img else ''
    return f'''<section class="phead{' phead--img' if img else ''}">
  <div class="wrap phead__in">
    <div class="phead__txt">{c}<h1>{title}</h1><p class="lead">{lead}</p></div>{art}
  </div>
  <svg class="phead__road" viewBox="0 0 1200 40" preserveAspectRatio="none" aria-hidden="true"><path d="M0 20 H1200"/></svg>
</section>'''


def why_list():
    return '<ul class="why">' + ''.join(f'<li><span class="why__ic">{icon(i)}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in WHY) + '</ul>'


def service_rows(pg, full=False):
    if not full:  # compact grid for the home page
        cards = ''.join(f'''<li><a class="svcard" href="{pg.u('our-services#' + key)}">
      <div class="svcard__img"><img src="{pg.u(img)}" alt="" loading="lazy"></div>
      <h3>{t}</h3><p>{d.split('. ')[0].rstrip('.')}.</p></a></li>''' for key, t, img, alt, d in SERVICES)
        return f'<ul class="svgrid">{cards}</ul>'
    out = ''
    for key, t, img, alt, d in SERVICES:
        cta = f'<a class="textlink" href="{pg.u("schedule-a-ride")}?ride={esc(t)}">Request this ride{icon("arrow")}</a>' if key != 'partners' else f'<a class="textlink" href="{pg.u("contact-us")}">Talk with us about partnering{icon("arrow")}</a>'
        out += f'''<li class="svc" id="{key}">
      <div class="svc__img"><img src="{pg.u(img)}" alt="{alt}" loading="lazy"></div>
      <div class="svc__txt"><h3>{t}</h3><p>{d}</p>{cta}</div>
    </li>'''
    return f'<ul class="svcs">{out}</ul>'


def trips():
    return '<ul class="chips">' + ''.join(f'<li>{icon("check")}{t}</li>' for t in TRIPS) + '</ul>'


def steps():
    return '<ol class="steps">' + ''.join(f'<li><h3>{t}</h3><p>{d}</p></li>' for t, d in STEPS) + '</ol>'


def reviews():
    return '<div class="quotes">' + ''.join(f'''<figure class="quote">
      <div class="stars" aria-label="5 out of 5 stars">{icon('star', 'st') * 5}</div>
      <blockquote><p>“{q}”</p></blockquote>
      <figcaption><strong>{n}</strong>{f'<span>{r}</span>' if r else ''}</figcaption>
    </figure>''' for q, n, r in REVIEWS) + '</div>'


def door_to_door(pg):
    items = [
        ('Trained, compassionate drivers', 'Trained in passenger assistance and safety, and patient with anyone who needs extra time or care.'),
        ('Accessible vehicles', 'Our vehicles are equipped to help passengers who use walkers, canes or wheelchairs.'),
        ('Door-to-door support', 'We don’t just pull up to the curb. We help you from your home, into the vehicle and into your destination.'),
        ('Recurring rides', 'Standing schedules for ongoing treatments like dialysis or therapy, so you don’t have to call every time.'),
    ]
    lis = ''.join(f'<li>{icon("check")}<div><h3>{t}</h3><p>{d}</p></div></li>' for t, d in items)
    return f'''<section class="sec">
  <div class="wrap split">
    <div class="split__img"><img src="{pg.u('assets/img/ramp.webp')}" alt="A passenger in a wheelchair on a vehicle lift" loading="lazy" width="1200" height="1500"></div>
    <div class="split__txt">
      <h2>More than a ride to the curb</h2>
      <p class="split__lead">From the moment we knock to the moment you’re settled back home, you’re treated with patience, dignity and understanding.</p>
      <ul class="d2d">{lis}</ul>
    </div>
  </div>
</section>'''


def cta_band(pg, title='Need a ride to an appointment?', text='Call us or send a ride request. We’ll confirm your trip and take care of the rest.'):
    return f'''<section class="band">
  <div class="wrap band__in">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="band__actions">
      <a class="btn btn--light" href="{pg.u('schedule-a-ride')}">Schedule a ride</a>
      <a class="btn btn--ghost-light" href="tel:{B['tel']}">{icon('phone')}Call {B['phone']}</a>
    </div>
  </div>
</section>'''


def article_cards(pg, items):
    out = ''.join(f'''<article class="acard"><a class="acard__link" href="{pg.u(s)}">
      <div class="acard__img"><img src="{pg.u(img)}" alt="" loading="lazy"></div>
      <h3>{t}</h3><p>{d}</p></a></article>''' for s, t, img, d in items)
    return f'<div class="acards">{out}</div>'


def contact_list():
    hrs = ''.join(f'{d}: {h}<br>' for d, h in HOURS)
    return f'''<ul class="clist">
      <li>{icon('phone')}<div><p class="clist__k">Phone</p><a href="tel:{B['tel']}">{B['phone']}</a></div></li>
      <li>{icon('mail')}<div><p class="clist__k">Email</p><a href="mailto:{B['email']}">{B['email']}</a></div></li>
      <li>{icon('pin')}<div><p class="clist__k">Office</p><a href="{B['map']}" target="_blank" rel="noopener">{B['street']}, {B['city']}</a></div></li>
      <li>{icon('clock')}<div><p class="clist__k">Hours</p><p>{hrs}</p></div></li>
      <li>{icon('id')}<div><p class="clist__k">NPI (for insurance use)</p><p>{B['npi']}</p></div></li>
    </ul>'''


def simple_form(subject='Website message'):
    return f'''<form class="form" data-form data-subject="{subject}" data-email="{B['email']}" novalidate>
    <div class="field"><label for="f-name">Your name <span class="opt">(required)</span></label><input id="f-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="f-phone">Phone number <span class="opt">(required)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
    <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
    <div class="field"><label for="f-msg">Your message</label><textarea id="f-msg" name="message" rows="4"></textarea></div>
    <p class="form__err" role="alert" data-form-err></p>
    <button class="btn btn--primary btn--block" type="submit">Send message</button>
    <p class="form__note">This opens your email app with your details filled in, ready to send.</p>
  </form>'''


def ride_form():
    rides = ['Doctor’s appointments', 'Physical therapy', 'Dialysis', 'Chemotherapy or infusion', 'Lab work or tests', 'Hospital discharge',
             'Daily errands', 'Veteran transportation', 'Something else']
    opts = ''.join(f'<option>{r}</option>' for r in rides)
    return f'''<form class="form form--ride" data-form data-subject="Ride request" data-email="{B['email']}" novalidate>
    <fieldset class="form__group"><legend>About you</legend>
      <div class="field-row">
        <div class="field"><label for="f-name">Your name <span class="opt">(required)</span></label><input id="f-name" name="name" autocomplete="name" required></div>
        <div class="field"><label for="f-phone">Phone number <span class="opt">(required)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
      </div>
      <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>
      <div class="field"><label for="f-who">Who is riding?</label><select id="f-who" name="who"><option>Me</option><option>A family member or friend</option><option>A patient or client (for facilities)</option></select></div>
    </fieldset>
    <fieldset class="form__group"><legend>About the trip</legend>
      <div class="field"><label for="f-ride">Where are you going?</label><select id="f-ride" name="ride">{opts}</select></div>
      <div class="field-row">
        <div class="field"><label for="f-date">Date</label><input id="f-date" name="date" type="date" data-min-today></div>
        <div class="field"><label for="f-time">Appointment time</label><input id="f-time" name="time" type="time"></div>
      </div>
      <div class="field"><label for="f-pickup">Pick-up address</label><input id="f-pickup" name="pickup" autocomplete="street-address"></div>
      <div class="field"><label for="f-dest">Destination name and address</label><input id="f-dest" name="dest"></div>
      <fieldset class="field"><legend>Mobility</legend>
        <div class="radios">
          <label><input type="radio" name="mobility" value="Walks without help" checked> Walks without help</label>
          <label><input type="radio" name="mobility" value="Uses a cane or walker"> Cane or walker</label>
          <label><input type="radio" name="mobility" value="Uses a wheelchair"> Wheelchair</label>
        </div></fieldset>
      <fieldset class="field"><legend>How often?</legend>
        <div class="radios">
          <label><input type="radio" name="repeat" value="One-time ride" checked> One-time ride</label>
          <label><input type="radio" name="repeat" value="Recurring ride"> Recurring ride</label>
        </div></fieldset>
      <fieldset class="field"><legend>Payment</legend>
        <div class="radios">
          <label><input type="radio" name="pay" value="Insurance" checked> Insurance</label>
          <label><input type="radio" name="pay" value="Private pay"> Private pay</label>
          <label><input type="radio" name="pay" value="Not sure"> Not sure</label>
        </div></fieldset>
      <div class="field"><label for="f-msg">Anything else we should know?</label><textarea id="f-msg" name="message" rows="3"></textarea></div>
    </fieldset>
    <p class="form__err" role="alert" data-form-err></p>
    <button class="btn btn--primary btn--block btn--lg" type="submit">Send ride request</button>
    <p class="form__note">This opens your email app with your trip details filled in. Your ride is booked once we call you to confirm it.</p>
  </form>'''


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
ROUTE_SVG = '''<svg class="route__svg" viewBox="0 0 320 250" aria-hidden="true">
  <path class="route__track" d="M40 210 C 40 140, 120 150, 150 110 S 250 60, 280 40"/>
  <path class="route__line" pathLength="1" d="M40 210 C 40 140, 120 150, 150 110 S 250 60, 280 40"/>
  <circle class="route__stop" cx="40" cy="210" r="9"/><circle class="route__stop route__stop--mid" cx="150" cy="110" r="7"/><circle class="route__stop route__stop--end" cx="280" cy="40" r="11"/>
</svg>'''


def home():
    pg = Page('')
    chips = trips()
    body = f'''
<section class="hero">
  <div class="wrap hero__in">
    <div class="hero__txt">
      <p class="hero__kicker">{icon('flag')}Veteran-owned transportation in Jacksonville, NC</p>
      <h1>Safe, on-time rides to every appointment.</h1>
      <p class="lead">Faithful Rides provides non-emergency medical transportation that puts your comfort, safety and schedule first. We help you from your door, into the vehicle and into your appointment — then bring you home.</p>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="{pg.u('schedule-a-ride')}">Schedule a ride</a>
        <a class="btn btn--outline btn--lg" href="tel:{B['tel']}">{icon('phone')}Call {B['phone']}</a>
      </div>
      <ul class="hero__facts">
        <li>{icon('wheel')}Wheelchair, walker and cane friendly</li>
        <li>{icon('card')}Most major insurances accepted</li>
      </ul>
    </div>
    <div class="hero__art">
      <div class="hero__photo"><img src="{pg.u('assets/img/hero-lift.webp')}" alt="A driver helping a smiling passenger in a wheelchair onto a van lift" width="1400" height="933" fetchpriority="high"></div>
      <div class="route">
        <p class="route__title">Door to door, every ride</p>
        <ol class="route__stops">
          <li><strong>We pick you up at home</strong><span>and help you into the vehicle</span></li>
          <li><strong>We walk you in</strong><span>to your appointment</span></li>
          <li><strong>We bring you home</strong><span>safely, on time</span></li>
        </ol>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap">{why_list()}</div>
</section>

<section class="sec sec--sky">
  <div class="wrap">
    <div class="sec__head sec__head--row">
      <div><h2>Where we can take you</h2><p>Routine appointments, therapy, hospital discharge or everyday errands — dependable rides for individuals, caregivers and healthcare providers.</p></div>
      <a class="textlink" href="{pg.u('our-services')}">All services{icon('arrow')}</a>
    </div>
    {service_rows(pg)}
    <div class="trips"><h3>Common trips</h3>{chips}</div>
  </div>
</section>

{door_to_door(pg)}

<section class="sec sec--sky">
  <div class="wrap">
    <div class="sec__head"><h2>Booking is simple</h2><p>Most rides are set up with one phone call.</p></div>
    {steps()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head"><h2>What riders say</h2></div>
    {reviews()}
  </div>
</section>

<section class="sec sec--sky">
  <div class="wrap cover">
    <div class="cover__txt">
      <h2>Using insurance for rides</h2>
      <p>We accept most major insurances. Many Medicare Advantage plans include transportation to medical appointments, and we may be able to provide those rides depending on your plan’s network. Private pay is always an option.</p>
      <dl class="npi"><dt>Our NPI for insurance use</dt><dd>{B['npi']}</dd></dl>
      <p><a class="textlink" href="{pg.u('newsroom')}">Read: Medicare vs. Medicare Advantage{icon('arrow')}</a></p>
    </div>
    <div class="cover__img"><img src="{pg.u('assets/img/medicare.webp')}" alt="An older woman and her daughter smiling together" loading="lazy" width="975" height="585"></div>
  </div>
</section>

<section class="sec" id="contact">
  <div class="wrap contact">
    <div class="contact__info">
      <h2>Contact us to schedule service</h2>
      <p>Give us a call or send your information and we’ll be in touch.</p>
      {contact_list()}
    </div>
    {simple_form()}
  </div>
</section>

<section class="sister">
  <div class="wrap sister__in">
    {icon('care')}
    <p><strong>Need help at home, too?</strong> Our sister company, Rapture Ready Home Care, provides in-home caregivers for seniors and adults from the same College Street office.</p>
    <a class="textlink" href="{B['sister']}" target="_blank" rel="noopener">Visit Rapture Ready{icon('arrow')}</a>
  </div>
</section>'''
    return pg, shell(pg, 'Non-Emergency Medical Transportation in Jacksonville, NC | Faithful Rides',
                     'Veteran-owned non-emergency medical transportation in Jacksonville, NC. Door-to-door rides to doctor visits, therapy, dialysis and errands. Wheelchair friendly. Most insurances accepted.', body)


def services():
    pg = Page('our-services')
    faq = [
        ('Do you help passengers who use a wheelchair?', 'Yes. Our vehicles are equipped to help passengers who use walkers, canes or wheelchairs, and our drivers are trained in passenger assistance.'),
        ('Can I set up rides on a regular schedule?', 'Yes. We offer recurring ride scheduling for ongoing treatments like dialysis or therapy.'),
        ('Do you take insurance?', f'We accept most major insurances, and private pay is welcome. Call {B["phone"]} and we’ll help you understand your options. Our NPI for insurance use is {B["npi"]}.'),
        ('Is this an ambulance service?', 'No. We provide non-emergency transportation for people who need help getting to care but don’t need an ambulance. In an emergency, call 911.'),
        ('Can a family member book a ride for a parent?', 'Absolutely. Many of our rides are scheduled by caregivers, family members and healthcare providers.'),
    ]
    faq_html = ''.join(f'<details class="faq__item"><summary>{q}<span class="faq__plus" aria-hidden="true"></span></summary><div class="faq__a"><p>{a}</p></div></details>' for q, a in faq)
    body = page_head(pg, 'Our services', 'Reliable non-emergency transportation near Jacksonville, NC. We promise to get you to your destination on time and in comfort, with courteous drivers every time.', img='assets/img/driver-smile.webp') + f'''
<section class="sec sec--flush">
  <div class="wrap">{service_rows(pg, True)}</div>
</section>
<section class="sec sec--sky">
  <div class="wrap trips trips--page"><h2>Trips we make every week</h2>{trips()}</div>
</section>
{door_to_door(pg)}
<section class="sec sec--sky">
  <div class="wrap"><div class="sec__head"><h2>How to schedule a ride</h2></div>{steps()}</div>
</section>
<section class="sec">
  <div class="wrap faq"><h2>Common questions</h2><div class="faq__list">{faq_html}</div></div>
</section>
{cta_band(pg)}'''
    return pg, shell(pg, 'NEMT Services in Jacksonville, NC | Faithful Rides',
                     'Rides to doctor appointments, physical therapy, dialysis, errands and veteran appointments in Jacksonville, NC. Healthcare partner transportation with HIPAA-aware drivers.', body, 'our-services')


def about():
    pg = Page('about-us')
    body = page_head(pg, 'About Faithful Rides', 'Safe, reliable transportation you can count on — from a veteran-owned, family-oriented team that cares about the community it serves.', img='assets/img/visit.webp') + f'''
<section class="sec sec--flush">
  <div class="wrap prose-2">
    <h2>Driven by care, guided by faith</h2>
    <div class="prose">
      <p class="big">At Faithful Rides, we believe transportation is more than getting from one place to another. It’s about connection, care and commitment.</p>
      <p>We specialize in non-emergency medical transportation that puts your comfort, safety and schedule first. Whether you need a ride to a routine appointment, a therapy session or a hospital discharge, our professional drivers ensure timely, courteous service — every time.</p>
      <p>We serve individuals, healthcare providers and caregivers with the dependable support they deserve: compassionate, punctual, flexible, committed and safe.</p>
    </div>
  </div>
</section>
<section class="sec sec--sky">
  <div class="wrap"><div class="sec__head"><h2>Why choose Faithful Rides</h2></div>{why_list()}</div>
</section>
<section class="sec">
  <div class="wrap"><div class="sec__head"><h2>What riders say</h2></div>{reviews()}</div>
</section>
<section class="sister">
  <div class="wrap sister__in">
    {icon('care')}
    <p><strong>Part of a caring family of services.</strong> Our sister company, Rapture Ready Home Care, provides in-home caregivers for seniors and adults in and around Jacksonville.</p>
    <a class="textlink" href="{B['sister']}" target="_blank" rel="noopener">Visit Rapture Ready{icon('arrow')}</a>
  </div>
</section>
{cta_band(pg)}'''
    return pg, shell(pg, 'About Us | Faithful Rides, Jacksonville NC', 'Faithful Rides is a veteran-owned, family-oriented non-emergency medical transportation company in Jacksonville, NC.', body, 'about-us', 'assets/img/visit.webp')


def schedule():
    pg = Page('schedule-a-ride')
    body = page_head(pg, 'Schedule a ride', 'Tell us about the trip. We’ll call you to confirm the details, and we’ll be there on time.') + f'''
<section class="sec sec--flush">
  <div class="wrap reqpage">
    <div>{ride_form()}</div>
    <aside class="req__aside">
      <div class="req__card">
        <h2>Prefer to call?</h2>
        <p>Most rides are booked with one phone call.</p>
        <a class="btn btn--primary btn--block" href="tel:{B['tel']}">{icon('phone')}{B['phone']}</a>
        <p class="req__hours">{hours_html()}</p>
      </div>
      <div class="req__card req__card--quiet">
        <h2>Have these ready</h2>
        <ul class="ticks"><li>{icon('check')}Appointment date and time</li><li>{icon('check')}Pick-up and destination addresses</li><li>{icon('check')}Walker, cane or wheelchair needs</li><li>{icon('check')}Insurance card, if using insurance</li></ul>
      </div>
      <p class="req__911">In a medical emergency, call 911.</p>
    </aside>
  </div>
</section>'''
    return pg, shell(pg, 'Schedule a Ride | Faithful Rides, Jacksonville NC', 'Request a non-emergency medical ride in Jacksonville, NC. Tell us the date, time and addresses and we’ll call to confirm.', body, None)


def contact():
    pg = Page('contact-us')
    body = page_head(pg, 'Contact us', 'Questions about a ride, insurance or partnering with us? We’re glad to help.') + f'''
<section class="sec sec--flush">
  <div class="wrap contact">
    <div class="contact__info"><h2>Reach our office</h2>{contact_list()}</div>
    {simple_form()}
  </div>
</section>
<section class="mapwrap">
  <iframe title="Map of 625 College St., Jacksonville, NC" src="https://maps.google.com/maps?q=625+College+St.,+Jacksonville,+NC+28540&z=15&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>'''
    return pg, shell(pg, 'Contact Us | Faithful Rides, Jacksonville NC', f'Call {B["phone"]} or email {B["email"]}. 625 College St., Jacksonville, NC 28540.', body, 'contact-us')


def community():
    pg = Page('community-on-the-move')
    body = page_head(pg, 'Community on the Move', 'Serving our community, one ride at a time. Guides for riders, caregivers and healthcare partners — rooted in compassion, dignity and trust.', img='assets/img/road.webp') + f'''
<section class="sec sec--flush">
  <div class="wrap">{article_cards(pg, ARTICLES)}</div>
</section>
{cta_band(pg)}'''
    return pg, shell(pg, 'Community on the Move | Faithful Rides Blog', 'Helpful guides about non-emergency medical transportation, Medicare and getting to care in Jacksonville, NC.', body, 'community-on-the-move', 'assets/img/road.webp')


def resources():
    pg = Page('resources')
    links = [
        ('Onslow County Senior Services', 'Programs and support services for older adults in Onslow County.', 'https://www.onslowcountync.gov/538/Senior-Services'),
        ('Medicare.gov', 'Compare plans and check what your coverage includes.', 'https://www.medicare.gov/'),
    ]
    ext = ''.join(f'<li><a href="{h}" target="_blank" rel="noopener"><span class="comm__t">{t}</span><span class="comm__d">{d}</span></a></li>' for t, d, h in links)
    body = page_head(pg, 'Rider resources', 'Everything you need to plan a ride, understand your coverage and find help close to home.') + f'''
<section class="sec sec--flush">
  <div class="wrap comm">
    <div class="comm__intro">
      <h2>Before you call</h2>
      <p>Having these details ready makes booking quick:</p>
      <ul class="ticks ticks--lg"><li>{icon('check')}Appointment date, time and address</li><li>{icon('check')}Where we should pick you up</li><li>{icon('check')}Whether you use a walker, cane or wheelchair</li><li>{icon('check')}If the ride repeats, like dialysis or therapy</li><li>{icon('check')}Your insurance card, if using insurance</li></ul>
      <p><a class="btn btn--primary" href="{pg.u('schedule-a-ride')}">Schedule a ride</a></p>
    </div>
    <div>
      <h2 class="h-sm">Helpful links</h2>
      <ul class="comm__list">{ext}</ul>
    </div>
  </div>
</section>
<section class="sec sec--sky">
  <div class="wrap"><div class="sec__head"><h2>Guides from our team</h2></div>{article_cards(pg, ARTICLES)}</div>
</section>'''
    return pg, shell(pg, 'Rider Resources | Faithful Rides', 'Plan your ride, understand Medicare transportation benefits and find local senior resources in Onslow County.', body, None)


def render_blocks(pg, blocks, skip):
    out, in_list, rows, dropped = [], False, [], set()
    def close():
        nonlocal in_list, rows
        if in_list: out.append('</ul>'); in_list = False
    for b in blocks:
        k = b[0]
        if k != 'li': close()
        if k in ('img', 'bg'):
            continue
        t = re.sub(r'href="@@([^"]*)"', lambda m: f'href="{pg.u(m.group(1).strip("/"))}"', b[1])
        t = t.replace('Faithfull', 'Faithful')
        plain = re.sub(r'<[^>]+>', '', t).strip()
        if plain.lower() in ('learn more', 'read more'):
            continue
        key = plain.lower().rstrip('?.!')
        if k == 'h2' and key in skip:
            continue
        if k == 'h2':
            out.append(f'<h2>{t}</h2>')
        elif k == 'h3':
            out.append(f'<h3>{t}</h3>' if len(plain) < 90 else f'<p class="big">{t}</p>')
        elif k == 'li':
            if not in_list: out.append('<ul>'); in_list = True
            out.append(f'<li>{t}</li>')
        else:
            if plain.count('|') >= 2:
                continue  # the old pipe-text table; rebuilt as a real table in article()
            out.append(f'<p>{t}</p>')
    close()
    return '\n'.join(out)


def article(meta, data):
    slug, title, img, dek = meta
    pg = Page(slug)
    blocks = data['blocks']
    skip = {re.sub(r'<[^>]+>', '', b[1]).strip().lower().rstrip('?.!') for b in blocks if b[0] == 'h2'}
    skip = {s for s in skip if s in (title.lower().rstrip('?.!'), 'community news & updates', 'community news &amp; updates',
                                   '5 key benefits of non-emergency medical transportation for senior citizens',
                                   'nemt 101: everything you need to know about our services',
                                   'understanding medicare vs. medicare advantage what you need to know')}
    if slug == 'newsroom':
        # the old newsroom page opened with a general intro; keep the article itself
        i = next(i for i, b in enumerate(blocks) if b[0] == 'h2' and 'Medicare' in b[1])
        blocks = blocks[i:]
    content = render_blocks(pg, blocks, skip)
    if slug == 'newsroom':
        table = '''<div class="tablewrap"><table><thead><tr><th scope="col">Question</th><th scope="col">Why it matters</th></tr></thead><tbody>
<tr><td>Do you have regular medical appointments?</td><td>Transportation benefits may be essential.</td></tr>
<tr><td>Do you prefer the freedom to choose your providers?</td><td>Traditional Medicare may offer more flexibility.</td></tr>
<tr><td>Are extra benefits like dental, vision or hearing important?</td><td>Medicare Advantage may include these.</td></tr>
<tr><td>Would having transportation covered reduce stress for you or your caregiver?</td><td>Medicare Advantage may be a strong fit.</td></tr>
</tbody></table></div>'''
        content = re.sub(r'(<h2>Choosing the Right Plan for Your Needs</h2>\s*<p>When selecting a healthcare plan, consider:</p>)', r'\1' + table.replace('\\', r'\\'), content)
    others = [a for a in ARTICLES if a[0] != slug]
    body = f'''
<article class="post">
  <header class="post__head wrap">
    <p class="crumb"><a href="{pg.u('community-on-the-move')}">{icon('back')}Community on the Move</a></p>
    <h1>{title}</h1>
    <p class="lead">{dek}</p>
  </header>
  <div class="post__hero wrap"><img src="{pg.u(img)}" alt="" width="1200" height="800"></div>
  <div class="post__body wrap-narrow prose">
    {content}
    <aside class="post__cta">
      <p><strong>Faithful Rides</strong> provides door-to-door non-emergency medical transportation in Jacksonville, NC.</p>
      <p><a class="btn btn--primary" href="{pg.u('schedule-a-ride')}">Schedule a ride</a> <a class="btn btn--outline" href="tel:{B['tel']}">{icon('phone')}{B['phone']}</a></p>
    </aside>
  </div>
</article>
<section class="sec sec--sky">
  <div class="wrap"><div class="sec__head"><h2>Keep reading</h2></div>{article_cards(pg, others)}</div>
</section>'''
    return pg, shell(pg, f'{title} | Faithful Rides', dek, body, 'community-on-the-move', img)


def privacy():
    pg = Page('privacy-policy')
    body = page_head(pg, 'Privacy policy', 'How this website handles your information. Last updated September 28, 2026.') + f'''
<section class="sec sec--flush">
  <div class="wrap-narrow prose">
    <h2>What we collect</h2>
    <p>This website does not collect personal information on its own. When you use our contact or ride request forms, your details are placed into an email in your own email app. Nothing is sent until you choose to send that email to {B['email']}.</p>
    <p>If you call, email or send us a message, we use what you share only to respond to you and to arrange transportation.</p>
    <h2>Cookies and tracking</h2>
    <p>This website does not use advertising or tracking cookies. If you change the text size, your browser remembers that choice on your own device. You can clear it at any time in your browser settings.</p>
    <h2>Protecting your information</h2>
    <p>We use appropriate practices to protect the information you share with us against unauthorized access, alteration, disclosure or destruction. Please don’t send medical records by email.</p>
    <h2>Other websites</h2>
    <p>Our pages link to other websites, such as Medicare.gov, Onslow County and Google Maps. We don’t control those sites and aren’t responsible for their content or privacy practices.</p>
    <h2>Changes to this policy</h2>
    <p>We may update this policy from time to time. When we do, we’ll change the date at the top of this page.</p>
    <h2>Contact us</h2>
    <p>Faithful Rides LLC<br>{B['street']}<br>{B['city']}<br><a href="tel:{B['tel']}">{B['phone']}</a><br><a href="mailto:{B['email']}">{B['email']}</a></p>
  </div>
</section>'''
    return pg, shell(pg, 'Privacy Policy | Faithful Rides', 'How the Faithful Rides website handles your information.', body)


def not_found():
    pg = Page('')
    body = f'''<section class="phead"><div class="wrap phead__in"><div class="phead__txt">
<h1>We couldn’t find that page</h1><p class="lead">The page may have moved when our website was updated. Try one of these, or call us at <a href="tel:{B['tel']}">{B['phone']}</a>.</p>
<p class="hero__actions"><a class="btn btn--primary" href="/">Go to the home page</a> <a class="btn btn--outline" href="/schedule-a-ride/">Schedule a ride</a></p></div></div></section>'''
    h = shell(pg, 'Page not found | Faithful Rides', 'Page not found.', body)
    h = h.replace('href="./', 'href="/').replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    h = re.sub(r'href="([a-z0-9-]+)/(\?[^"]*)?"', r'href="/\1/\2"', h)
    return h


def write(pg, text):
    d = os.path.join(ROOT, pg.slug) if pg.slug else ROOT
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(text)
    return pg.slug


def main():
    data = json.load(open(os.path.join(ROOT, '_src', 'articles.json')))
    slugs = [write(*f()) for f in (home, services, about, schedule, contact, community, resources, privacy)]
    for meta in ARTICLES:
        slugs.append(write(*article(meta, data[meta[0]])))
    open(os.path.join(ROOT, '404.html'), 'w').write(not_found())
    today = date.today().isoformat()
    urls = ''.join(f'<url><loc>{DOMAIN}/{s + "/" if s else ""}</loc><lastmod>{today}</lastmod></url>' for s in slugs)
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    print(f'built {len(slugs)} pages')


if __name__ == '__main__':
    main()
