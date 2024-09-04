from pii_detective import pii_detect_layer1,pii_detect_layer2
file='Adhr_crdSubro.pdf'
print(pii_detect_layer2(file))
print(pii_detect_layer1(file))
