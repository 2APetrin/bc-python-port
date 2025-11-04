import py4j.GatewayServer;

public class BCPythonPortGateway {
    static GatewayServer server = new GatewayServer();;

    public static void main(String[] args) {
        server.start();

        System.out.println("Py4J Gateway Server started");
    }
}
