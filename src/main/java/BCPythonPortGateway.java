import py4j.GatewayServer;

public class BCPythonPortGateway {
    static GatewayServer server = new GatewayServer();;

    public static void main(String[] args) {
        if (args.length < 1) {
            System.err.println("[Java][ERROR] Expected: <token>");
            System.exit(1);
        }

        String token = args[0];

        GatewayServer server = new GatewayServer.GatewayServerBuilder()
                                                .authToken(token)
                                                .build();
        server.start();
        System.out.println("[Java][INFO] Py4J Gateway started");
    }
}
