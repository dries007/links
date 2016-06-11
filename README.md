# links
A simple homebrew private URL shortener

Deployed at [l.dries007.net](//l.dries007.net)

Yes, yes, I know, PHP. It works for what I need and I know it well enough. It's also easy to setup.

If you find leaks, please do tell!

## nginx config

Use this location block in your nginx config file:

```nginx
location ~* "^/(?<id>[a-z0-7]{10})(?:/(?<plugin>[a-z0-7_-]*))?/?$" {
    rewrite ^/.*$ /router.php?id=$id&plugin=$plugin;
}

location /api/ {
    rewrite ^/api/([a-z0-9]+)$ /api/$1.php;
}
```

Note: You need to change the regex if you want to use a different id size. I picked 10 because its enough to have LOTs of ids, but it also fits in a small QR code. 

If you want to also redirect uncaught url's to the index page:

```nginx
location / {
    try_files $uri $uri/ /index.php;
}
```
    
## SQL for setup

Don't forget to replace the `links_` with the correct table prefix and change the column sizes.

```sql
CREATE TABLE `links_tokens` (
  `id` int(10) UNSIGNED NOT NULL,
  `token` char(10) NOT NULL,
  `identity` char(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `links_urls` (
  `id` char(10) NOT NULL,
  `enabled` tinyint(1) NOT NULL DEFAULT '1',
  `url` varchar(2048) NOT NULL,
  `token` int(10) UNSIGNED NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

ALTER TABLE `links_tokens`
  ADD PRIMARY KEY (`id`);
  
ALTER TABLE `links_urls`
  ADD PRIMARY KEY (`id`(10)),
  ADD KEY `token` (`token`);

ALTER TABLE `links_tokens`
  MODIFY `id` int(10) UNSIGNED NOT NULL AUTO_INCREMENT;
  
ALTER TABLE `links_urls`
  ADD CONSTRAINT `tokens` FOREIGN KEY (`token`) REFERENCES `links_tokens` (`id`);
```