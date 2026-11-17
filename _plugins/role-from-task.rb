# Sets each post's role from its task (_data/roles.yml), so a post's header needs only `task:`.

module Jekyll
  class RoleFromTask < Generator
    safe true
    priority :highest

    def generate(site)
      role_of = {}
      (site.data["roles"] || []).each { |r| (r["tasks"] || []).each { |t| role_of[t["id"]] = r["id"] } }
      site.posts.docs.each do |post|
        role = role_of[post.data["task"]]
        post.data["role"] = role if role
      end
    end
  end
end
