from os import environ

SESSION_CONFIGS = [
    dict(
        name='Agranov_voting',
        display_name="Agranov et al (2018) - LabPolls",
        num_demo_participants=3,
        app_sequence=['Agranov_etal_2018']
    ),
    dict(
        name='Agranov_voting_NoPolls',
        display_name="Agranov et al (2018) - NoPolls",
        num_demo_participants=3,
        app_sequence=['Agranov_etal_2018_NoPolls']
    ),
    dict(
        name='Agranov_voting_PerfectPolls',
        display_name="Agranov et al (2018) - PerfectPolls",
        num_demo_participants=3,
        app_sequence=['Agranov_etal_2018_PerfectPolls']
    ),
    dict(
        name='Levine_voting',
        display_name="Levine and Palfrey (2007)",
        num_demo_participants=3,
        app_sequence=['Levine_Palfrey_2007']
    ),
]

ROOMS = [
    dict(
        name='test_room',
        display_name='Experimental Economics Test Lab',
        # participant_label_file='_rooms/test.txt',
        # use_secure_urls=True
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1.00, participation_fee=0.00, doc=""
)

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '2rs_5k#u+%#ngc(nui!(&x$aj%7)gsie__-51vck(5d7clpqg^'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree']
