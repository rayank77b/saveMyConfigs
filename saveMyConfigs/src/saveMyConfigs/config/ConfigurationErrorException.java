package saveMyConfigs.config;

public class ConfigurationErrorException extends Exception {

	private static final long serialVersionUID = 1763246814645747L;

	public String errors;
	
	public ConfigurationErrorException() {
		super();
	}

	public ConfigurationErrorException(String message) {
		super(message);
		this.errors=message;
	}
	
}
