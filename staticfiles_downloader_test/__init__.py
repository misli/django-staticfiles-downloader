staticfiles_urls = {
    # use only url
    'my_app/js/jquery-3.2.1.min.js': 'https://code.jquery.com/jquery-3.2.1.min.js',
    # or use url and checksum
    'my_app/js/jquery-2.2.4.min.js': (
        'https://code.jquery.com/jquery-2.2.4.min.js',
        'sha384',
        'rY/jv8mMhqDabXSo+UCggqKtdmBfd3qC2/KvyTDNQ6PcUJXaxK1tMepoQda4g5vB',
    ),
}
