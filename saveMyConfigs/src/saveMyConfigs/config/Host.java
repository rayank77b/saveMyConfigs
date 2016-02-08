package saveMyConfigs.config;

public class Host {
	private String ipAddress;
	private String userName;
	private String password;
	private String remotePath;
	private String localPath;
	
	/**
	 * @param ipAddress
	 * @param userName
	 * @param password
	 * @param remotePath
	 * @param localPath
	 */
	public Host(String ipAddress, String userName, String password, String remotePath, String localPath) {
		this.ipAddress = ipAddress;
		this.userName = userName;
		this.password = password;
		this.remotePath = remotePath;
		this.localPath = localPath;
	}
	/**
	 * @return the ipAddress
	 */
	public String getIpAddress() {
		return ipAddress;
	}
	/**
	 * @param ipAddress the ipAddress to set
	 */
	public void setIpAddress(String ipAddress) {
		this.ipAddress = ipAddress;
	}
	/**
	 * @return the userName
	 */
	public String getUserName() {
		return userName;
	}
	/**
	 * @param userName the userName to set
	 */
	public void setUserName(String userName) {
		this.userName = userName;
	}
	/**
	 * @return the password
	 */
	public String getPassword() {
		return password;
	}
	/**
	 * @param password the password to set
	 */
	public void setPassword(String password) {
		this.password = password;
	}
	/**
	 * @return the remotePath
	 */
	public String getRemotePath() {
		return remotePath;
	}
	/**
	 * @param remotePath the remotePath to set
	 */
	public void setRemotePath(String remotePath) {
		this.remotePath = remotePath;
	}
	/**
	 * @return the localPath
	 */
	public String getLocalPath() {
		return localPath;
	}
	/**
	 * @param localPath the localPath to set
	 */
	public void setLocalPath(String localPath) {
		this.localPath = localPath;
	}
	
	
	
}
