package saveMyConfigs.config;

import java.util.List;

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
	
	public static SSHServerConfig setSSHServerConfiguration(ReadINI iniObject) throws ConfigurationErrorException {
		// FIXME: at moment we use only 1 git-server for save configurations
		List<String> list = iniObject.getItem("ssh-server");
		if(list.size()==0) {
			throw new ConfigurationErrorException("errors on read git server configuration");
		}
		String username=null;
		String password=null;
		String ip=null;
		for(String s : list) {
			String[] s2 = s.split("=");
			if(s2[0].trim().equals("username")) 
				username=s2[1].trim();
			if(s2[0].trim().equals("password")) 
				password=s2[1].trim();
			if(s2[0].trim().equals("ipaddress")) 
				ip=s2[1].trim();
		}
		if(username==null || password==null || ip==null) {
			throw new ConfigurationErrorException("errors on read ssh server configuration, element lose");
		}
		return new SSHServerConfig(ip, username, password);
		
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

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "SSHServerConfig [ipAddress=" + ipAddress + ", userName=" + userName + ", password=" + password + "]";
	}
	
	

}
