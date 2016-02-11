package saveMyConfigs;

import java.io.IOException;

import com.jcraft.jsch.ChannelSftp;
import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.SftpException;

public class WorkFileFromSSH {
	private String host;
	private String user;
	private String password;
	private String repopath;
	private String remotepath;
	private SSHConnect sshc;
	
	public WorkFileFromSSH(String host, String user, String password, String remotepath, String repopath) {
		this.host = host;
		this.user = user;
		this.password = password;
		this.repopath = repopath;
		this.remotepath = remotepath;
		
		this.sshc = new SSHConnect(this.user, this.password, this.host);
	}
	
	public void copy() throws JSchException, IOException, SftpException {
		this.sshc.connect();
		System.out.println("ok connected");
		ChannelSftp csftp = sshc.openSFTPChannel();
		System.out.println("sftp opened");
		System.out.println(remotepath);
		System.out.println(repopath);
		this.sshc.copyFileSFTPChannel(this.remotepath, this.repopath, csftp );
		System.out.println("copied");
	}
	
	

}
