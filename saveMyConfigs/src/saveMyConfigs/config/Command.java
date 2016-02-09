package saveMyConfigs.config;

/*
[file-bluber-config.xml]
host=bluber
remotepath=/path/config.xml
localpath=bluber1/config.xml
*/
public class Command {
	private String host;
	private String remotePath;
	private String localPath;
	private String how;
	
	public Command(String host, String remotePath, String localPath, String how) {
		super();
		this.host = host;
		this.remotePath = remotePath;
		this.localPath = localPath;
		this.how = how;
	}

	public String getHost() {
		return host;
	}

	public String getRemotePath() {
		return remotePath;
	}

	public String getLocalPath() {
		return localPath;
	}
	
	public String getHow() {
		return how;
	}

}
