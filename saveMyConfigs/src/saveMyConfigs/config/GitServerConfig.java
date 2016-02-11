package saveMyConfigs.config;

import java.util.List;

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
	private String repoPath;
	private String remoteUrl;

	public GitServerConfig(String userName, String password, String remotePath, String remoteUrl) {
		this.userName = userName;
		this.password = password;
		this.repoPath = remotePath;
		this.remoteUrl = remoteUrl;
	}
	

	public static GitServerConfig setGitServerConfiguration(ReadINI iniObject) throws ConfigurationErrorException {
		// FIXME: at moment we use only 1 git-server for save configurations
		List<String> list = iniObject.getItem("git-configs");
		if(list.size()==0) {
			throw new ConfigurationErrorException("errors on read git server configuration");
		}
		String username=null;
		String password=null;
		String repopath=null;
		String remote=null;
		for(String s : list) {
			String[] s2 = s.split("=");
			if(s2[0].trim().equals("username")) 
				username=s2[1].trim();
			if(s2[0].trim().equals("password")) 
				password=s2[1].trim();
			if(s2[0].trim().equals("repopath")) 
				repopath=s2[1].trim();
			if(s2[0].trim().equals("remote")) 
				remote=s2[1].trim();
		}
		if(username==null || password==null || repopath==null || remote==null) {
			throw new ConfigurationErrorException("errors on read git server configuration, element lose");
		}
		return new GitServerConfig(username, password, repopath, remote);
		
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
	public String getRepoPath() {
		return repoPath;
	}

	/**
	 * @return the remoteUrl
	 */
	public String getRemoteUrl() {
		return remoteUrl;
	}


	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "GitServerConfig [userName=" + userName + ", password=" + password + ", remotePath=" + repoPath
				+ ", remoteUrl=" + remoteUrl + "]";
	}
	
}
