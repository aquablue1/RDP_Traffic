import requests
import ipaddress


class ResearchIP(object):
    def __init__(self, ip, abuse_days=180):
        self.IP = ipaddress.ip_address(ip)
        self.abuse_api_key = 'uSmlOI2zdCrsEJ0hgJyguGymmWBcjHDyPZ8uJtNH'
        self.days = abuse_days
        self.abuse_log = []
        self.geo_log = []

    def find_abuse(self):
        request = 'https://www.abuseipdb.com/check/%s/json?key=%s&days=%s' \
                  % (self.IP, self.abuse_api_key, self.days)
        rtm = requests.get(request)

        try:
            data = rtm.json()
            if data == []:
                # means this IP has never been reported in the abuse db.
                ResearchIP.print_to_log("%s: No Abuse Reported." %self.IP)
            elif isinstance(data, dict):
                log = []
                msg = "Alert!"
                country = data['country']
                category = data['category']
                created = data['created']
                is_whited = data['isWhitelisted']
                log.append(str(self.IP))
                log.append(country)
                log.append(str(is_whited))
                log.append(created)
                # log.append(category)
                log.append(msg)
                # Write all useful info into log (list) and print them.
                for num in category:
                    cate_str = ResearchIP.get_cat(num)
                    log.append(cate_str)
                    ResearchIP.print_to_log('\t'.join(log))
                    # DEBUG
                    # print('\t'.join(log))
                    # END DEBUG
                    log.remove(cate_str)
            else:
                # means some suspecious records were found.
                for record in data:
                    log = []
                    msg = "Alert!"
                    country = record['country']
                    category = record['category']
                    created = record['created']
                    is_whited = record['isWhitelisted']
                    log.append(str(self.IP))
                    log.append(country)
                    log.append(str(is_whited))
                    log.append(created)
                    # log.append(category)
                    log.append(msg)
                    # Write all useful info into log (list) and print them.
                    for num in category:
                        cate_str = ResearchIP.get_cat(num)
                        log.append(cate_str)
                        ResearchIP.print_to_log('\t'.join(log))
                        # DEBUG
                        # print('\t'.join(log))
                        # END DEBUG
                        log.remove(cate_str)

        except (ValueError, KeyError, TypeError):
            error_log = []
            ip_address = ("Error when looking for %s:" % self.IP)
            error_log.append(ip_address)
            ResearchIP.print_to_error('\n'.join(error_log))

    @staticmethod
    def print_to_log(str):
        with open('../results/ip_report.log', 'a') as f:
            f.write(str + '\n')

    @staticmethod
    def print_to_error(str):
        with open('../results/ip_error.log', 'a') as f:
            f.write('Error Warning: %s \n' % str)



    @staticmethod
    def get_cat(x):
        return {
            3: 'Frad_Orders',
            4: 'DDoS_Attack',
            5: 'FTP_Brute-Force',
            6: 'Ping of Death',
            7: 'Phishing',  # phishing web and/or email
            8: 'Fraud VoIP',
            9: 'Open_Proxy',
            10: 'Web_Spam',
            11: 'Email_Spam',
            12: 'Blog_Spam',
            13: 'Conjunctive category',
            14: 'Port_Scan',
            15: 'Hacking',
            16: 'SQL Injection',
            17: 'Spoofing',
            18: 'Brute_Force',
            19: 'Bad_Web_Bot',
            20: 'Exploited_Host',
            21: 'Web_App_Attack',
            22: 'SSH',
            23: 'IoT_Targeted',
        }.get(
            x,
            '*UNDEFINED ABUSE TYPE.*')

    def find_basic(self):
        request = 'http://www.ip-api.com/json/%s' %(self.IP)
        rtm = requests.get(request)
        try:
            record = rtm.json()
            if record['status']=="success":
                log = []
                as_name = record['as']
                country = record['country']
                city = record['city']
                region = record['region']
                lat = record['lat']
                lon = record['lon']
                isp = record['isp']
                org = record['org']

                log.append(str(self.IP))
                log.append(country)
                log.append(city)
                log.append(region)
                log.append(isp)
                log.append(str(lat))
                log.append(str(lon))
                log.append(org)
                log.append(as_name)

                ResearchIP.print_to_log('\t'.join(log))

            elif record['status'] == "fail":
                ResearchIP.print_to_log("NOT FOUND Warning: IP: %s Not Found in the database." % self.IP)

            else:
                ResearchIP.print_to_log("Server returns Uncontrolled status msg: %s." % record['status'])

        except (ValueError, KeyError, TypeError):
            ResearchIP.print_to_error("Error occures when looking up %s." %self.IP)


if __name__ == '__main__':
    # main()
    # get_report("11.31.101.127")
    ip_str = "8.8.8.8"
    ip_str = "5.39.221.13"
    ip = ResearchIP(ip_str)
    ip.find_basic()
    ip.find_abuse()
