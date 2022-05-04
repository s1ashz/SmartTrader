

config_SOS = 0.0125
config_SS = 0.98
config_OS = 1.01

SO_vol = 30


BO_ss = 1

BO_price = 0.151462360761087
BO_vol = 300
BO_size = BO_vol / BO_price


SO1_price = BO_price * (1 - config_SOS)
SO1_vol = SO_vol
SO1_size = SO1_vol / SO1_price

SO2_price = SO1_price * (1 - config_SOS * config_SS )
SO2_vol = SO1_vol * config_OS
SO2_size = SO2_vol / SO2_price

SO3_price = SO2_price * (1 - config_SOS * config_SS )
SO3_vol = SO2_vol * config_OS
SO3_size = SO3_vol / SO3_price

SO4_price = SO3_price * (1 - config_SOS * config_SS )
SO4_vol = SO3_vol * config_OS
SO4_size = SO4_vol / SO4_price

print(BO_price, BO_size)
print(SO1_price, SO1_size)
print(SO2_price, SO2_size)
print(SO3_price, SO3_size)
print(SO4_price, SO4_size)



my_map = {}

my_map[2] = "xico"
my_map[4] = "Filipe"
my_map[1] = "Matheus"


print("")
print(my_map[min(my_map)])