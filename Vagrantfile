Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu2204"

  def base_python_provision(vm)
    vm.vm.provision "shell", inline: <<-SHELL
      sudo apt update -y
      sudo apt install -y python3 python3-pip sshpass
    SHELL
  end

  config.vm.define "db" do |db|
    db.vm.network "private_network", ip: "192.168.200.10"

    db.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus = 1
      vb.name = "db"
    end

    db.vm.provision "shell", inline: <<-SHELL
      sudo apt update
      sudo apt install -y postgresql postgresql-contrib
      sudo -u postgres psql -c "CREATE USER vagrant WITH PASSWORD 'vagrant';"
      sudo -u postgres psql -c "CREATE DATABASE flaskdb OWNER vagrant;"
      sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/*/main/postgresql.conf
      echo "host all all 0.0.0.0/0 md5" | sudo tee -a /etc/postgresql/*/main/pg_hba.conf
      sudo systemctl restart postgresql
    SHELL
  end

  config.vm.define "elasticsearch" do |es|
    es.vm.network "private_network", ip: "192.168.200.11"

    es.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus = 2
      vb.name = "elasticsearch"
    end

    es.vm.provision "shell", inline: <<-SHELL
      wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
      sudo apt install -y apt-transport-https
      echo "deb https://artifacts.elastic.co/packages/8.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-8.x.list
      sudo apt update
      sudo apt install -y elasticsearch kibana
      sudo systemctl enable elasticsearch --now
      sudo systemctl enable kibana --now
    SHELL
  end

  config.vm.define "app" do |app|
    app.vm.network "private_network", ip: "192.168.200.12"

    app.vm.provider "virtualbox" do |vb|
      vb.memory = 3072
      vb.cpus = 2
      vb.name = "app"
    end

    app.vm.provision "shell", inline: <<-SHELL
      sudo apt update -y
      sudo apt install -y nginx filebeat
      sudo systemctl enable nginx --now
      sudo filebeat modules enable system nginx
      sudo sed -i 's|#hosts: \["localhost:9200"\]|hosts: ["192.168.200.11:9200"]|' /etc/filebeat/filebeat.yml
      sudo systemctl enable filebeat --now
    SHELL
  end

  config.vm.define "client" do |client|
    client.vm.network "private_network", ip: "192.168.200.13"

    client.vm.provider "virtualbox" do |vb|
      vb.memory = 1024
      vb.cpus = 1
      vb.name = "client"
    end

    base_python_provision(client)
  end

  config.vm.define "wireshark" do |ws|
    ws.vm.network "private_network", ip: "192.168.200.14"

    ws.vm.provider "virtualbox" do |vb|
      vb.memory = 2048
      vb.cpus = 1
      vb.name = "wireshark"
    end

    base_python_provision(ws)

    ws.vm.provision "shell", inline: <<-SHELL
      sudo apt install -y wireshark tcpdump
    SHELL
  end
end
