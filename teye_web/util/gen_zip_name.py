#coding=utf-8

def gen_zip_name(domain):
	'''
	'''
	common_list = ["demo","wwwtest","test","www","wwwbak","wwwroot","w","wbak","web","webroot","root","default","home","homeroot","1","111","123"]

	black_list = ["com","cn","org"]

	d_list = domain.split(".")
	#过滤掉IP地址
	#域名:www.watscan.com
	common_list.append(domain)
	#域名:watscan.com,watscan_com
	new_domain_1 = ".".join(d_list[1:])
	new_domain_2 = "_".join(d_list[1:])
	common_list.append(new_domain_1)
	common_list.append(new_domain_2)
	#域名:www_watscan_com
	new_domain_3 = "_".join(d_list)
	common_list.append(new_domain_3)


	for item in d_list:
		if item=="www":
			continue
		if item in black_list:
			continue
		common_list.append(item)

	return common_list

