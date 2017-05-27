// Flex sensor test program

// Sensor pin - GND
// Sensor pin - Analog In 0, with 10K resistor to +5V

int fsr1Pin = 13; // FSR is connected to digital 1
int fsr2Pin = 12;
int fsr3Pin = 9;
int fsr4Pin = 8;
int fsr5Pin = 7;
int fsr6Pin = 6;
int fsr7Pin = 5;
int fsr8Pin = 4;
int flag;
int fsrReading;      // the analog reading from the FSR resistor divider
int lt = 2;
boolean checker;

void setup()
{
    // initialize serial communications
    Serial.begin(9600); //Baud rate is 9600 for serial communication
    //pinMode(fsr1Pin, INPUT);
    //pinMode(fsr2Pin, INPUT);
    //pinMode(fsr3Pin, INPUT);
    Serial.println("CLEARDATA");
    Serial.println("LABEL, TIME ,Finger 1,Finger 2,Finger 3,Finger 4,Finger 5,Finger 6,Finger 7,Finger 8");
    flag = 1;
}

void loop()
{
    int sensor1,sensor2,sensor3,sensor4,sensor5,sensor6,sensor7,sensor8, deg1,deg2,deg3,deg4,deg5,deg6,deg7,deg8,fsr1Reading,fsr2Reading,fsr3Reading,fsr4Reading,fsr5Reading,fsr6Reading,fsr7Reading,fsr8Reading, f1 = 1 , f2 = 1, f3 = 1, f4 = 1, f5 = 1, f6 = 1, f7 = 1, f8 = 1, lefthumb;

    // read the voltage from the voltage divider (sensor plus resistor)
    sensor1 = analogRead(0);
    sensor2 = analogRead(1);
    sensor3 = analogRead(2);
    sensor4 = analogRead(3);
    sensor5 = analogRead(4);
    sensor6 = analogRead(5);
    sensor7 = analogRead(6);
    sensor8 = analogRead(7);
    

    // convert the voltage reading to inches
    // the first two numbers are the sensor values for straight (768) and bent (853)
    // the second two numbers are the degree readings we'll map that to (0 to 90 degrees)
    deg1 = map(sensor1, 350,650 , 0, 1024);
    deg2 = map(sensor2, 261,544 , 0, 1024);
    deg3 = map(sensor3, 300,600 , 0, 1024);
    deg4 = map(sensor4, 300,500 , 0, 1024);
    deg5 = map(sensor5, 350,550 , 0, 1024);
    deg6 = map(sensor6, 500,800 , 0, 1024);
    deg7 = map(sensor7, 350,650 , 0, 1024);
    deg8 = map(sensor8, 300,600 , 0, 1024);
    

    // print out the result
    //Serial.print("analog input: ");
    //Serial.print (sensor,DEC);
    //Serial.print("DATA,TIME,");
    
    //Serial.println(" DEGREE: ");
    fsr1Reading = digitalRead(fsr1Pin);
    fsr2Reading = digitalRead(fsr2Pin);
    fsr3Reading = digitalRead(fsr3Pin);
    fsr4Reading = digitalRead(fsr4Pin);
    fsr5Reading = digitalRead(fsr5Pin);
    fsr6Reading = digitalRead(fsr6Pin);
    fsr7Reading = digitalRead(fsr7Pin);
    fsr8Reading = digitalRead(fsr8Pin);
	lefthumb = digitalRead(lt);

  
    //Serial.println(fsr1Reading);
    if(fsr1Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
      Serial.print("3 ");
      Serial.println(deg1);
      //Serial.println (", , , , , , , "); //Print ASCII value 
      flag = 0;
      f1 = 0;
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if(fsr2Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
     Serial.print("2 ");
      //Serial.print(" , ");
      Serial.println(deg2);//Print ASCII value 
      //Serial.println(", , , , , ,");
      f2 = 0;
      flag = 0;
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if(fsr3Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
      Serial.print("1 ");
      //Serial.print (" , , ");
      Serial.println(deg3);
      //Serial.println(", , , , ,");
      flag = 0;
      f3 = 0;
       //Print ASCII value 
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if(fsr4Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
      Serial.print("0 ");
      //Serial.print (", , , ");
      Serial.println(deg4);
      //Serial.println(", , , ,");
      flag = 0;
      f4 = 0;
       //Print ASCII value 
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if(fsr5Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
      Serial.print("4 ");
//      Serial.print (", , , , ");
      Serial.println(deg5);
//      Serial.println(", , ,");
      flag = 0;
      f5 = 0;
       //Print ASCII value 
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if(fsr6Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
      Serial.print("5 ");
//      Serial.print (", , , , , ");
      Serial.println(deg6);
//      Serial.println(", ,");
      flag = 0;
      f6 = 0;
       //Print ASCII value 
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if(fsr7Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
      Serial.print("6 ");
//      Serial.print (", , , , , , ");
      Serial.println(deg7);
//      Serial.println(",");
      flag = 0;
      f7 = 0;
       //Print ASCII value 
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if(fsr8Reading <= 0)
    {
     // if(deg >=100 && deg <=1000)
      //{
      Serial.print("7 ");
//      Serial.print (", , , , , , , ");
      Serial.println(deg8);
      flag = 0;
      f8 = 0;
       //Print ASCII value 
      //Serial.print(",");
      //Serial.print("Analog reading = ");
      //Serial.print(fsrReading);
      //Serial.println("IT IS KEY : F");
    //}
    }
    if ((f1 && f2 && f3 && f4 && f5 && f6 && f7 && f8) && !flag)  
    {
    Serial.println("END");
    flag = 1;
  }
	if (lefthumb <= 0)
  {
    delay(500);
    while (digitalRead(lt) <= 0)
    {
      Serial.println("LTL");
      delay(1000);
      checker = true;
      //lefthumb = digitalRead(lt)
      }
      if (checker != true)
      {
        Serial.println("LTT");
        }
      if (checker == true)
      {
        Serial.println("LTL END");
        checker = false;
        }
      
      }
    // pause before taking the next reading
    delay(100); 
}
