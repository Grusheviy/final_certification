import java.io.FileWriter;
import java.io.IOException;
import java.util.PriorityQueue;
import java.util.Random;

// Класс игрушки с параметрами (id, имя и вес)
class Toy {
    private String id;
    private String name;
    private int weight;

    public Toy(String id, String name, int weight) {
        this.id = id;
        this.name = name;
        this.weight = weight;
    }

    // Методы для доступа к параметрам
    public String getId() {

        return id;
    }

    public String getName() {

        return name;
    }

    public int getWeight() {

        return weight;
    }
}

// Класс для управления приоритетной очередью
public class ToyCollection {
    private PriorityQueue<Toy> queue;

    public ToyCollection() {
        queue = new PriorityQueue<>((t1, t2) -> Integer.compare(t2.getWeight(), t1.getWeight()));
    }

    public void addToy(Toy toy) {
        queue.add(toy);
    } // Добавляем игрушку в очередь

    // Возвращаем случайную игрушку на основе случайно сгенерированного числа
    public Toy getRandomToy() {
        Random random = new Random();
        int randomNumber = random.nextInt(10) + 1;

        // Если число меньше 2, возвращаем игрушку с наибольшим весом из очереди.
        if (randomNumber <= 2) {
            System.out.println("\n" + "Случайно сгенерированное число: " + randomNumber);
            return queue.peek();

        // Если число находится между 2 и 4, он возвращаем игрушку с индексом 1
        } else if (randomNumber <= 4) {
            Toy[] toys = queue.toArray(new Toy[0]);
            System.out.println("\n" + "Случайно сгенерированное число: " + randomNumber);
            return toys[1];

        // Иначе возвращаем игрушку с индексом 2
        } else {
            Toy[] toys = queue.toArray(new Toy[0]);
            System.out.println("\n"+ "Случайно сгенерированное число: " + randomNumber);
            return toys[2];
        }
    }

    public static void main(String[] args) {
        // Создаем экземпляр класс ToyCollection и добавляем в него 3 игрушки
        ToyCollection toyQueue = new ToyCollection();
        toyQueue.addToy(new Toy("1", "Конструктор", 2));
        toyQueue.addToy(new Toy("2", "Робот", 2));
        toyQueue.addToy(new Toy("3", "Кукла", 6));

        // Создаем объект FileWriter для записи в файл
        try {
            FileWriter fileWriter = new FileWriter("output.txt");

            // Внутри цикла вызываем метод getRandomToy для получения случайно игрушки
            for (int i = 0; i < 10; i++) {
                Toy randomToy = toyQueue.getRandomToy();
                fileWriter.write(randomToy.getId() + " " + randomToy.getName() + "\n"); // И записываем ее id и имя в файл
                System.out.println("Случайно выбранный игрушка: " + randomToy.getId() + " " + randomToy.getName());
            }
            fileWriter.close();
            System.out.println("\n" + "Результаты записаны в файл output.txt.");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
