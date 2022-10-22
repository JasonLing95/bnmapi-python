import requests
import datetime

from .constants import BASE_CURRENCY, EXCHANGE_SESSION, PRODUCTS, URL


class BNM():
    """
    Python wrapper for OpenBNM open API
    """

    def _fetch(self, url: str) -> dict:
        """
        Function to handle request
        """
        headers = {'Accept': 'application/vnd.BNM.API.v1+json'}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            raise IOError(
                f'Request failed, response code {response.status_code}')
        return response.json()

    def _validate_date_format(self, date: str) -> None:
        """
        Function to validate date format YYYY-MM-DD
        """
        try:
            datetime.datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            raise ValueError(
                "incorrect date format '{}', should be YYYY-MM-DD".format(
                    date))

    def _validate_args(self, args) -> None:
        """
        Function to validate args: 2021 01
        """
        if len(args[0]) != 4:
            raise ValueError(
                "Incorrect year format '{}'. Format: e.g. 2021".format(
                    args[0]))
        elif not 0 < int(args[1]) < 13:
            raise ValueError(
                "Incorrect month format '{}'. Format: e.g. 1 or 01".format(
                    args[1]))
        else:
            pass

    def _validate_year(self, year: str) -> None:
        """
        Function to validate year format: 2021
        """
        if len(year) != 4:
            raise ValueError(
                "incorrect year format '{}'. Format: e.g. 2021".format(year))

    def base_rates(self, bank_code: str = False) -> dict:
        """
        Current Base Rates and Base Lending Rates for retail loans
        or financing facilities and Indicative Effective Lending Rates
        for a standard housing loan/home financing offered by
        financial institutions.
        """
        if not bank_code:
            return self._fetch(f'{URL}/base-rate')
        else:
            return self._fetch(f'{URL}/base-rate/{bank_code}')

    def daily_fx(self, *args) -> dict:
        """
        Daily foreign exchange turnover for all currencies
        including interbank and customer deals.

        Examples:
            - daily_fx()
            - daily_fx('2020-09-08')
            - daily_fx('2022', '01')
        """
        if len(args) == 0:
            return self._fetch(f'{URL}/fx-turn-over')
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(f'{URL}/fx-turn-over/date/{args[0]}')
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                f'{URL}/fx-turn-over/year/{args[0]}/month/{args[1]}')

    def exchange_rate(
            self,
            interval: str = False,
            base: str = False,
            currency: str = False,
            *args) -> dict:
        """
        Currency exchange rates from the Interbank Foreign Exchange Market
        in Kuala Lumpur. The price of selected countries currency
        in relation to Ringgit.
        """

        if not interval and not base and not currency and not args:
            return self._fetch(f'{URL}/exchange-rate')
        elif len(args) == 0:
            if interval and not base:
                values = ', '.join(BASE_CURRENCY)
                raise ValueError(
                    f'Missing base parameter. Accepted value: {values}')
            elif not interval and base:
                values = ', '.join(EXCHANGE_SESSION)
                raise ValueError(
                    f'Missing interval parameter. Accepted value: {values}')
            elif interval not in EXCHANGE_SESSION:
                values = ', '.join(EXCHANGE_SESSION)
                raise ValueError(
                    f'Incorrect interval session. Accepted value: {values}')
            elif base not in BASE_CURRENCY:
                values = ', '.join(BASE_CURRENCY)
                raise ValueError(
                    f'Incorrect base currency. Accepted value: {values}')
            elif interval and base and not currency:
                return self._fetch(
                    f'{URL}/exchange-rate?session={interval}&quote={base}')
            else:
                return self._fetch(
                    '{}/exchange-rate/{}?session={}&quote={}'.format(
                        URL, currency, interval, base
                    ))
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(
                '{}/exchange-rate/{}/date/{}?session={}&quote={}'.format(
                    URL, currency, args[0], interval, base
                ))
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                '{}/exchange-rate/{}/year/{}/month/{}?session={}&quote={}'
                .format(
                    URL, currency, args[0], args[1], interval, base
                ))
        else:
            raise Exception('Too many input arguments')

    def consumer_alert(self, keyword) -> dict:
        """
        A list of known companies and websites which are neither authorised
        nor approved under the relevant laws and regulations
        administered by BNM. (Based on information received by BNM).
        """
        if not keyword:
            return self._fetch('{URL}/consumer-alert')
        else:
            return self._fetch(f'{URL}/consumer-alert/{keyword}')

    def interbank_swap(self, *args) -> dict:
        """
        Daily interbank swap volume by tenure.

        Examples:
            - interbank_swap()
            - interbank_swap('2020-09-08')
            - interbank_swap('2022', '01')
        """
        if len(args) == 0:
            return self._fetch(f'{URL}/interbank-swap')
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(f'{URL}/interbank-swap/date/{args[0]}')
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                f'{URL}/interbank-swap/year/{args[0]}/month/{args[1]}')

    def interest_rate(self, product: str = False, *args) -> dict:
        """
        Daily interbank money market rates
        and volumes of transactions according to tenure. (2015 - present)

        e.g. product
        - money_market_operations
        - interbank
        - overall

        Examples:
            - interest_rate('overall', '2020-09-08')
            - interest_rate('overall', '2022', '01')
        """
        if not product:
            url = f'{URL}/interest-rate'
        elif product and not args:
            if product not in PRODUCTS:
                values = ', '.join(PRODUCTS)
                raise ValueError(
                    'Incorrect product value provided.'
                    f' Accepted value: {values}')
            return self._fetch(
                f'{URL}/interest-rate?product={product}')
        elif product and args:
            if len(args) == 1:
                self._validate_date_format(args[0])
                return self._fetch(
                    f'{URL}/interest-rate/date/{args[0]}?product={product}')
            elif len(args) == 2:
                self._validate_args(args)
                return self._fetch(
                    f'{URL}/interest-rate/year/{args[0]}/month/{args[1]}?product={product}')
            else:
                raise Exception('Too many parameters passed')

    def interest_volume(self, product: str = False, *args) -> dict:
        """
        Daily interbank money market
        rates and volumes of transactions
        according to tenure. (2015 - present)

        e.g. product
        - money_market_operations
        - interbank
        - overall

        Examples:
            - interest_volume('overall', '2020-09-08')
            - interest_volume('overall', '2022', '01')
        """
        if not product:
            url = f'{URL}/interest-volume'
        elif product and not args:
            if product not in PRODUCTS:
                values = ', '.join(PRODUCTS)
                raise ValueError(
                    'Incorrect product value provided.'
                    f' Accepted value: {values}')
            return self._fetch(f'{URL}/interest-volume?product={product}')
        elif product and args:
            if len(args) == 1:
                self._validate_date_format(args[0])
                return self._fetch(
                    f'{URL}/interest-volume/date/{args[0]}?product={product}')
            elif len(args) == 2:
                self._validate_args(args)
                return self._fetch(
                    f'{URL}/interest-volume/year/{args[0]}/month/{args[1]}?product={product}')
            else:
                raise Exception('Too many parameters passed')

    def islamic_interbank_rate(self, *args) -> dict:
        """
        Daily weighted average of
        Islamic interbank deposit rates for various tenures. (Jan 2015-present)

        Examples:
            - islamic_interbank_rate('2020-09-08')
            - islamic_interbank_rate('2022', '01')
        """
        if len(args) == 0:
            return self._fetch('{URL}/islamic-interbank-rate')
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(f'{URL}/islamic-interbank-rate/date/{args[0]}')
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                f'{URL}/islamic-interbank-rate/year/{args[0]}/month/{args[1]}')

    def kijang_emas(self, *args) -> dict:
        """
        Daily trading prices of Malaysia gold bullion coin.

        Examples:
            - kijang_emas('2020-09-08')
            - kijang_emas('2022', '01')
        """
        if len(args) == 0:
            return self._fetch('{URL}/kijang-emas')
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(f'{URL}/kijang-emas/date/{args[0]}')
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                f'{URL}/kijang-emas/year/{args[0]}/month/{args[1]}')

    def opr(self, year: str = False) -> dict:
        """
        Overnight Policy Rate (OPR)
        decided by the Monetary Policy Committee.

        Examples:
            - opr('2021')
        """
        if not year:
            return self._fetch(f'{URL}/opr')
        else:
            self._validate_year(year)
            return self._fetch(f'{URL}/opr/year/{year}')

    def renminbi(self, fx: bool) -> dict:
        """
        Indicative CNY/MYR forward prices for trade
        settlement and RMB deposit acceptance rates
        """
        if fx:
            return self._fetch(f'{URL}/renminbi-fx-forward-price')
        else:
            return self._fetch(f'{URL}/renminbi-deposit-acceptance-rate')

    def interbank_intraday_rate(self, *args) -> dict:
        """
        USD/MYR Interbank Intraday Rate
        USD/MYR interbank intraday highest and lowest rate.
        Rates are obtained from the best U.S. dollar against
        Malaysian ringgit interbank highest and lowest dealt rates
        by commercial banks on the specific date.

        Examples:
            - interbank_intraday_rate('2020-09-08')
            - interbank_intraday_rate('2022', '01')
        """
        if len(args) == 0:
            return self._fetch(f'{URL}/usd-interbank-intraday-rate')
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(f'{URL}/kl-usd-reference-rate/date/{args[0]}')
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                f'{URL}/usd-interbank-intraday-rate/year/{args[0]}/month/{args[1]}')

    def usd_reference_rate(self, *args) -> dict:
        """
        Kuala Lumpur USD/MYR Reference Rate
        A reference rate that is computed based on weighted average
        volume of the interbank USD/MYR FX spot rate transacted by
        the domestic financial institutions and published
        daily at 3:30 p.m.

        Examples:
            - usd_reference_rate('2020-09-08')
            - usd_reference_rate('2022', '01')
        """
        if len(args) == 0:
            return self._fetch(f'{URL}/kl-usd-reference-rate')
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(f'{URL}/kl-usd-reference-rate/date/{args[0]}')
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                f'{URL}/kl-usd-reference-rate/year/{args[0]}/month/{args[1]}')

    def overnight_rate(self, *args) -> dict:
        """
        Malaysia Overnight Rate - I

        Examples:
            - overnight_rate('2022-02-30')
            - overnight_rate('2022', '01')
        """
        if len(args) == 0:
            return self._fetch(f'{URL}/my-overnight-rate-i')
        elif len(args) == 1:
            self._validate_date_format(args[0])
            return self._fetch(f'{URL}/my-overnight-rate-i/date/{args[0]}')
        elif len(args) == 2:
            self._validate_args(args)
            return self._fetch(
                f'{URL}/my-overnight-rate-i/month/{args[1]}/year/{args[0]}')
        else:
            raise ValueError(
                'should be either one input date (e.g. 2022-03-10) '
                'or two inputs (month, year)')
