package saveMyConfigs.config;

/*
 [ssh-server]
ipaddress = 192.168.10.50
username = bla
password = 111111
 */
public class SSHServerConfig {
	private String ipAddress;
	private String userName;
	private String password;
	
	public SSHServerConfig(String ipAddress, String userName, String password) {
		this.ipAddress = ipAddress;
		this.userName = userName;
		this.password = password;
	}

	public String getIpAddress() {
		return ipAddress;
	}

	public String getUserName() {
		return userName;
	}

	public String getPassword() {
		return password;
	}
	
	

}
