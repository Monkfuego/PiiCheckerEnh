import re
from file_reader import read_text_from_file
from pii_regex import pii_regex,doc_pii_regex

def gstincheck(file):    
    matches = pii_regex['GSTIN'].findall(read_text_from_file(file))
    return len(matches), matches

def phonenumberindiacheck(file):
    matches = pii_regex['PhoneNumber_India'].findall(read_text_from_file(file))
    return len(matches), matches

def emailcheck(file):
    matches = pii_regex['Email'].findall(read_text_from_file(file))
    return len(matches), matches

def bankaccountindiacheck(file):
    matches = pii_regex['BankAccount_India'].findall(read_text_from_file(file))
    return len(matches), matches

def creditcardcheck(file):
    matches = pii_regex['CreditCard'].findall(read_text_from_file(file))
    return len(matches), matches

def ipv4check(file):
    matches = pii_regex['IPv4'].findall(read_text_from_file(file))
    return len(matches), matches

def ipv6check(file):
    matches = pii_regex['IPv6'].findall(read_text_from_file(file))
    return len(matches), matches

def ifsccheck(file):
    matches = pii_regex['IFSC'].findall(read_text_from_file(file))
    return len(matches), matches

def vehicleregistrationindiacheck(file):
    matches = pii_regex['VehicleRegistration_India'].findall(read_text_from_file(file))
    return len(matches), matches

def npsprancheck(file):
    matches = pii_regex['NPS_PRAN'].findall(read_text_from_file(file))
    return len(matches), matches

def aadharcardcheck(file):
    matches = doc_pii_regex['Aadhar Card'].findall(read_text_from_file(file))
    return len(matches), matches

def pancardcheck(file):
    matches = doc_pii_regex['Pan Card'].findall(read_text_from_file(file))
    return len(matches), matches

def voteridcheck(file):
    matches = doc_pii_regex['Voter Id'].findall(read_text_from_file(file))
    return len(matches), matches

def passportcheck(file):
    matches = doc_pii_regex['Passport'].findall(read_text_from_file(file))
    return len(matches), matches

def driverlicensecheck(file):
    matches = doc_pii_regex['Driver License'].findall(read_text_from_file(file))
    return len(matches), matches

def nregajobcardcheck(file):
    matches = doc_pii_regex['NREGA Job Card'].findall(read_text_from_file(file))
    return len(matches), matches
