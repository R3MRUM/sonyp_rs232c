from sonyp_rs232c import SonyHWXXES

x = SonyHWXXES.SonyHWXXES(port='COM2', verbose=True)

powerStatus = x.getStatusPower()

if powerStatus == 'Power On':
	x.rPowerOff()
elif powerStatus in ('Power Off','Standby'):
	x.rPowerOn()