package saveMyConfigs.config;

import java.util.List;
import java.util.Map;
import java.util.Set;

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
	
	public static void setHostConfiguration(ReadINI iniObject, Map<String, Host> hosts)  throws ConfigurationErrorException {
		Set<String> hostsKeys = iniObject.getKeys("host-.*");
		if(hostsKeys.size()==0) {
			throw new ConfigurationErrorException("errors on read hosts configuration");
		}
		for(String hostconfig : hostsKeys) {
			List<String> hostlist = iniObject.getItem(hostconfig);
			String hostname=null;
			String ip=null;
			String username=null;
			String password=null;
			for(String s : hostlist) {
				//System.out.println(s);
				String[] s2 = s.split("=");
				if(s2[0].trim().equals("username")) 
					username=s2[1].trim();
				if(s2[0].trim().equals("password")) 
					password=s2[1].trim();
				if(s2[0].trim().equals("host")) 
					hostname=s2[1].trim();
				if(s2[0].trim().equals("ipaddress")) 
					ip=s2[1].trim();
			}
			//System.out.println(hostconfig + " " +hostlist);
			if(username==null || password==null || hostname==null || ip==null) {
				throw new ConfigurationErrorException("errors on read host configuration, element 2lose");
			}
			
			hosts.put(hostname, new Host(hostname, ip, username, password));
		}
		if(hosts.size()==0) {
			throw new ConfigurationErrorException("errors on read hosts configuration, no hosts");
		}
	}
	
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
