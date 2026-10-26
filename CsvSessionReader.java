import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class CsvSessionReader {

    public List<Session> readCsv(String fileName) {

        List<Session> sessions = new ArrayList<>();

        try (BufferedReader br =
                     new BufferedReader(new FileReader(fileName))) {

            // Skip the header
            br.readLine();

            String line;

            while ((line = br.readLine()) != null) {

                String[] data = line.split(",");

                Session session = new Session(
                    data[0],
                    data[1],
                    data[2],
                    LocalDateTime.parse(data[3]),
                    LocalDateTime.parse(data[4]),
                    LocalDateTime.parse(data[5]),
                    Double.parseDouble(data[6]),
                    Boolean.parseBoolean(data[7])
                );

                sessions.add(session);
            }

        } catch (IOException | RuntimeException e) {
            System.out.println("Error reading CSV: " + e.getMessage());
        }

        return sessions;
    }
}