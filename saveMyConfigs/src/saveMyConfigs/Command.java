package saveMyConfigs;

import java.io.IOException;

import com.jcraft.jsch.JSchException;
import com.jcraft.jsch.SftpException;

import saveMyConfigs.config.CommandConfig;
import saveMyConfigs.config.ENV;
import saveMyConfigs.config.GitServerConfig;
import saveMyConfigs.config.HostConnfig;
import saveMyConfigs.config.SSHServerConfig;

public class Command {
	private String commandName;
	private String command;
	private CommandConfig commmandConfig;
	private GitServerConfig gitServerConfig;
	private SSHServerConfig sshServerConfig;
	private HostConnfig hostConfig;
	
	private ENV env;

	public Command(ENV env, String commandName) {
		this.env = env;
		this.commandName = commandName;
		this.gitServerConfig = this.env.getGitServer();
		this.sshServerConfig = this.env.getSSHServer();
		this.commmandConfig = this.env.getCommand(this.commandName);
		this.hostConfig = this.env.getHosts(this.commmandConfig.getHost());
		this.command = this.commmandConfig.getCommand();
	}
	
	public String getCommandName() {
		return commandName;
	}

	public void work() {
		if(this.command.equals("file")) {
			workFile();
		}
	}
	
	private void workFile() {
		String repoPath = this.gitServerConfig.getRepoPath();
		String host = this.hostConfig.getIpAddress();
		String user = this.hostConfig.getUserName();
		String pass = this.hostConfig.getPassword();
		String remoteFile = this.commmandConfig.getRemotePath();
		String localFile = this.commmandConfig.getLocalPath();
		WorkFileFromSSH wf = new WorkFileFromSSH(host, user, pass, remoteFile, repoPath+"/"+localFile );
		try {
			wf.copy();
		} catch (JSchException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		} catch (SftpException e) {
			e.printStackTrace();
		}
	}

	/* (non-Javadoc)
	 * @see java.lang.Object#toString()
	 */
	@Override
	public String toString() {
		return "Command \n["+ commandName + "\n\t " + commmandConfig + "\n\t "
				+ gitServerConfig + "\n\t " + sshServerConfig + "\n\t " + hostConfig + "\n\t "
				+ env + "]\n------------------------------------------------";
	}
	
	
	
	

}
