package saveMyConfigs.config;

/*
[git-configs]
username=name
password=pass1
repopath=/home/ray/path/toRepo.git
remote=http://bla:bla@domain.com:8080/git/TestConfig.git
 */
public class GitServerConfig {
	private String userName;
	private String password;
	private String remotePath;
	private String remoteUrl;

	public GitServerConfig(String userName, String password, String remotePath, String remoteUrl) {
		this.userName = userName;
		this.password = password;
		this.remotePath = remotePath;
		this.remoteUrl = remoteUrl;
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

	/**
	 * @return the remotePath
	 */
	public String getRemotePath() {
		return remotePath;
	}

	/**
	 * @return the remoteUrl
	 */
	public String getRemoteUrl() {
		return remoteUrl;
	}
}
