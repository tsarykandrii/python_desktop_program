using System;
using System.IO;
using System.Runtime.InteropServices;
using SLMessageServerLib;

namespace ModeTitleButton
{
    class Program
    {
        private const string _queueNameTemplate = "FDOnAir{0}";
        private const int WM_USER = 0x0400;
        private const int _noifyCmd = WM_USER + 200;

        private static string logFilePath = "app_mode_title.log";
        private static int maxLogFileSizeKB = 200; // Maximum log file size in kilobytes
        private static int maxLogFileCount = 3;    // Maximum number of log files

        private static void Main(string[] args)
        {
            // Check the number of command-line arguments
            if (args.Length < 4)
            {
                Log("Usage: ModeTitleButton.exe <computerName> <queueSend> <subject> <command>");
                return;
            }

            // Get the values of command-line arguments
            string computerName = args[0];
            string queueSend = args[1];
            string subject = args[2];
            string command = args[3];
            const string queueName = "TitleQueue";

            // Check and manage log files before starting
            ManageLogFiles();

            SLMSConnection connection = null;
            ISLMSQueue queue = null;

            try
            {

                // Establish a connection with the SLMS message server
                connection = new SLMSConnectionClass();
                object queueObject;
                SLMSErrorCode Code;
                int hr;

                // Create the queue name based on the template
                string fullQueueName = string.Format(_queueNameTemplate, queueName);
                // Create the queue on the message server
                connection.CreateQueue(out Code, out hr, fullQueueName, 0, 0, 0, 0, out queueObject);
                queue = queueObject as ISLMSQueue;

                if (queue != null)
                {
                    // Send a message to the queue
                    SendMessageToQueue(queue, computerName, queueSend, subject, command);
                    Marshal.ReleaseComObject(queue);
                }
                else
                {
                    Log("Failed to create the queue.");
                }
            }
            catch (COMException ex)
            {
                Log("COM Exception: " + ex.Message);
            }
            catch (Exception ex)
            {
                Log("Error: " + ex.Message);
            }
            finally
            {
                if (queue != null)
                    Marshal.ReleaseComObject(queue);
                if (connection != null)
                    Marshal.ReleaseComObject(connection);
            }
        }

        private static void SendMessageToQueue(ISLMSQueue queue, string computerName, string queueSend, string subject, string command)
        {
            SLMSErrorCode Code;
            int hr;
            int messageId = 0; // Set the appropriate message ID.
            // Send a message to the queue
            queue.SendMessage(out Code, out hr, messageId++, 0, 0, computerName, queueSend, subject, command);

            if (Code == SLMSErrorCode.mcSuccess)
            {
                Log("Message sent successfully.");
            }
            else
            {
                Log("Failed to send the message. Error Code: " + Code);
            }
        }

        private static void Log(string message)
        {
            try
            {
                // Check and manage log files before writing
                ManageLogFiles();

                // Write the message to the log file
                using (var writer = new StreamWriter(logFilePath, true))
                {
                    writer.WriteLine($"[{DateTime.Now}] {message}");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error while logging: " + ex.Message);
            }
        }

        private static void ManageLogFiles()
        {
            // Check if the log file exists and its size
            if (File.Exists(logFilePath))
            {
                FileInfo fileInfo = new FileInfo(logFilePath);
                if (fileInfo.Length > maxLogFileSizeKB * 1024)
                {
                    // Rename the current log file with a timestamp
                    string timeStamp = DateTime.Now.ToString("yyyyMMddHHmmss");
                    string newFileName = $"app_mode_title_{timeStamp}.log";
                    File.Move(logFilePath, newFileName);
                }
            }

            // Check the number of log files and delete excess files
            string[] logFiles = Directory.GetFiles(".", "app_mode_title_*.log");
            if (logFiles.Length > maxLogFileCount)
            {
                Array.Sort(logFiles);
                for (int i = 0; i < logFiles.Length - maxLogFileCount + 1; i++)
                {
                    File.Delete(logFiles[i]);
                }
            }
        }
    }
}
