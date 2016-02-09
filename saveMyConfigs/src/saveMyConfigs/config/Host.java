package saveMyConfigs.config;

/*
[host-bluber]
host=bluber
ipaddress=192.168.10.12
username=name
password=pass2
 */
public class Host {
	private String hostName;
	private String ipAddress;
	private String userName;
	private String password;
	
	public Host(String hostName, String ipAddress, String userName, String password) {
		this.hostName = hostName;
		this.ipAddress = ipAddress;
		this.userName = userName;
		this.password = password;
	}
	
	/**
	 * @return the hostName
	 */
	public String getHostName() {
		return hostName;
	}
	/**
	 * @return the ipAddress
	 */
	public String getIpAddress() {
		return ipAddress;
	}
	/**
	 * @return the userName
	 */
	public String getUserName() {
		return userName;
	}
	/**
	 * @return the password
	 */
	public String getPassword() {
		return password;
	}
}
